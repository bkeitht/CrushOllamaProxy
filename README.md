# **CrushOllamaProxy**
Integrate **Charm Crush** with **local Ollama / OpenWebUI models** using a lightweight FastAPI proxy.

---

## **Overview**
This project provides a **Python FastAPI-based proxy** that:
- Translates **OpenAI API calls** from Charm Crush into **Ollama API calls**.
- Lets you run **local LLMs** (via Ollama / OpenWebUI) inside Crush without paid APIs.
- Supports **any Ollama model** you have installed — including **Qwen 2.5 Coder 32B** for Swift and code generation.

---

## **Architecture**

    ┌────────────────────┐
    │    Charm Crush      │
    │  (OpenAI Client)    │
    └─────────┬───────────┘
              │ OpenAI API Calls
              ▼
    ┌────────────────────┐
    │   FastAPI Proxy     │
    │ (Crush ↔ Ollama)    │
    └─────────┬───────────┘
              │ Ollama API Calls
              ▼
    ┌────────────────────┐
    │  Ollama / OpenWebUI │
    │  (Local LLM Server) │
    └────────────────────┘

---

## **1. Requirements**

### **Operating System**
- macOS or Linux (tested on macOS Sequoia and Ubuntu 24.04)

### **Installed Software**
- **Python 3.10+** (`python3 --version`)
- **pip** (`pip --version`)
- **Ollama** installed and running with your models (`ollama list`)
- **Charm Crush** installed
- **OpenWebUI** running locally or accessible on your LAN

---

## **2. Install Dependencies**

We’ll create a **virtual environment** to avoid messing with system Python.

    # Go to your working folder
    cd ~/Documents

    # Create a folder for the proxy
    mkdir openwebui-proxy
    cd openwebui-proxy

    # Create a Python virtual environment
    python3 -m venv openwebui-proxy-venv

    # Activate it
    source openwebui-proxy-venv/bin/activate

    # Install dependencies
    pip install fastapi uvicorn requests

---

## **3. Run Proxy**

    # Activate virtual environment (if not already active)
    source ~/Documents/openwebui-proxy/openwebui-proxy-venv/bin/activate

    # Run proxy
    OLLAMA_URL="http://<server>:11434" \
    OLLAMA_MODEL="qwen2.5-coder:32b" \
    python openwebui_proxy.py

The proxy will then listen on:

    http://<server>:5000/v1

---

## **4. Configure Charm Crush**

Edit:

    ~/.local/share/crush/providers.json

Example for Qwen2.5-Coder:32B via local proxy:

    {
      "providers": {
        "openrouter": {
          "name": "Local Ollama (Qwen2.5-Coder:32B)",
          "id": "openrouter",
          "api_key": "",
          "api_endpoint": "http://<server>:5000/v1",
          "type": "openai",
          "default_large_model_id": "qwen2.5-coder:32b",
          "default_small_model_id": "qwen2.5-coder:32b",
          "models": [
            {
              "id": "qwen2.5-coder:32b",
              "name": "Qwen 2.5 Coder 32B",
              "cost_per_1m_in": 0,
              "cost_per_1m_out": 0,
              "context_window": 256000,
              "default_max_tokens": 16000,
              "can_reason": true,
              "has_reasoning_efforts": false,
              "supports_attachments": false
            }
          ]
        }
      },
      "models": {
        "large": {
          "model": "qwen2.5-coder:32b",
          "provider": "openrouter",
          "max_tokens": 16000
        },
        "small": {
          "model": "qwen2.5-coder:32b",
          "provider": "openrouter",
          "max_tokens": 16000
        }
      }
    }

---

## **5. Make `providers.json` Read-Only** (Prevents Crush Overwriting)

    chmod 444 ~/.local/share/crush/providers.json

If you need to edit it later:

    chmod 644 ~/.local/share/crush/providers.json
    nano ~/.local/share/crush/providers.json
    chmod 444 ~/.local/share/crush/providers.json

---

## **Tips**
- Ensure **Ollama** is running before starting the proxy.
- You can change `OLLAMA_MODEL` to use any installed model.
- If using **OpenWebUI**, make sure it’s accessible via LAN if not running locally.
