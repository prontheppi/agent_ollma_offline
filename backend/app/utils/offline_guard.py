from __future__ import annotations

from urllib.parse import urlparse


LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def is_localhost(value: str) -> bool:
    return value.strip().lower() in LOCAL_HOSTS


def is_localhost_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return True
    return parsed.hostname in LOCAL_HOSTS


def validate_backend_host(host: str) -> None:
    if host != "127.0.0.1":
        raise ValueError("Backend must bind only to 127.0.0.1.")


def validate_ollama_host(host: str) -> None:
    if host != "127.0.0.1":
        raise ValueError("Ollama host must be 127.0.0.1.")


def validate_local_url(url: str) -> None:
    if not is_localhost_url(url):
        raise ValueError(f"External URL is blocked in offline mode: {url}")


def validate_runtime_config(settings) -> None:
    validate_backend_host(settings.backend.host)
    validate_ollama_host(settings.ollama.host)

    if not settings.security.offline_only:
        raise ValueError("offline_only must remain enabled.")
    if settings.security.allow_external_urls:
        raise ValueError("External URLs are not allowed.")
    if settings.security.telemetry_enabled:
        raise ValueError("Telemetry must remain disabled.")
    if settings.security.auto_update_enabled:
        raise ValueError("Auto-update must remain disabled.")

    validate_local_url(settings.ollama.base_url)
