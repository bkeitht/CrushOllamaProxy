from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import uvicorn
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://<server>:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:32b")

app = FastAPI()

def get_ollama_models():
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags")
        resp.raise_for_status()
        data = resp.json()
        return [
            {"id": m["name"], "object": "model", "owned_by": "ollama", "permission": []}
            for m in data.get("models", [])
        ]
    except:
        return [{"id": DEFAULT_MODEL, "object": "model", "owned_by": "ollama", "permission": []}]

@app.get("/v1/models")
@app.get("/api/v1/models")
async def list_models():
    return {"object": "list", "data": get_ollama_models()}

def call_ollama_chat(payload):
    try:
        model = payload.get("model", DEFAULT_MODEL)
        messages = payload.get("messages", [])
        ollama_payload = {"model": model, "messages": messages, "stream": False}
        resp = requests.post(f"{OLLAMA_URL}/api/chat", json=ollama_payload)
        resp.raise_for_status()
        data = resp.json()
        return {
            "id": f"{model}-proxy",
            "object": "chat.completion",
            "model": model,
            "choices": [
                {"index": 0, "message": {"role": "assistant", "content": data.get("message", {}).get("content", "")}, "finish_reason": "stop"}
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/v1/chat/completions")
@app.post("/api/v1/chat/completions")
async def chat_completions(request: Request):
    payload = await request.json()
    result = call_ollama_chat(payload)
    if "error" in result:
        return JSONResponse(content=result, status_code=500)
    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
