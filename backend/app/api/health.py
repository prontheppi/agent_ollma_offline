from fastapi import APIRouter

from app.config import get_settings
from app.database.db import check_database
from app.services.ollama_service import check_ollama_status


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()
    database_status = check_database(settings)
    ollama_status = check_ollama_status(settings)

    return {
        "status": "ok" if database_status["ok"] else "degraded",
        "backend": {
            "host": settings.backend.host,
            "port": settings.backend.port,
        },
        "database": database_status,
        "ollama": ollama_status,
        "offline_mode": {
            "enabled": settings.security.offline_only,
            "external_urls_allowed": settings.security.allow_external_urls,
            "telemetry_enabled": settings.security.telemetry_enabled,
            "auto_update_enabled": settings.security.auto_update_enabled,
        },
        "models": {
            "llm": settings.ollama.llm_model,
            "embedding": settings.ollama.embedding_model,
        },
    }
