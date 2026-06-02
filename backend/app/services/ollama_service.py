from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from app.config import AppSettings
from app.utils.offline_guard import validate_local_url


LOCAL_MODEL_MISSING_MESSAGE = (
    "Local model not found. Please install the offline model pack before using AI features."
)


def _request_json(url: str, payload: dict | None = None, timeout: float = 2.0) -> dict:
    validate_local_url(url)
    data = None
    headers = {"Content-Type": "application/json"}
    method = "GET"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        method = "POST"
    request = Request(url, data=data, headers=headers, method=method)
    with urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    return json.loads(body) if body else {}


def check_ollama_status(settings: AppSettings) -> dict:
    url = f"{settings.ollama.base_url}/api/tags"
    try:
        payload = _request_json(url)
    except (OSError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "url": settings.ollama.base_url,
            "message": "Ollama is not reachable on 127.0.0.1:11434.",
            "error": str(exc),
        }

    models = [item.get("name") for item in payload.get("models", []) if item.get("name")]
    return {
        "ok": True,
        "url": settings.ollama.base_url,
        "models": models,
        "llm_model_found": settings.ollama.llm_model in models,
        "embedding_model_found": settings.ollama.embedding_model in models,
    }


def list_local_models(settings: AppSettings) -> dict:
    status = check_ollama_status(settings)
    if not status.get("ok"):
        return {"ok": False, "models": [], "message": status.get("message")}
    return {"ok": True, "models": status.get("models", [])}


def test_model(model: str, settings: AppSettings) -> dict:
    models = list_local_models(settings)
    if not models.get("ok"):
        return {"ok": False, "model": model, "message": models.get("message")}
    if model not in models.get("models", []):
        return {"ok": False, "model": model, "message": LOCAL_MODEL_MISSING_MESSAGE}
    return {"ok": True, "model": model, "message": "Local model is available."}


def generate_answer(prompt: str, model: str, settings: AppSettings) -> dict:
    url = f"{settings.ollama.base_url}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    return _request_json(url, payload=payload, timeout=120.0)


def generate_embedding(text: str, model: str, settings: AppSettings) -> list[float]:
    url = f"{settings.ollama.base_url}/api/embeddings"
    payload = {"model": model, "prompt": text}
    response = _request_json(url, payload=payload, timeout=60.0)
    return response.get("embedding", [])
