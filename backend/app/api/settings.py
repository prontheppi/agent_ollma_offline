from fastapi import APIRouter, HTTPException
import yaml

from app.config import AppSettings, get_settings, reload_settings
from app.schemas.settings_schema import SettingsUpdate
from app.services.ollama_service import check_ollama_status, list_local_models, test_model
from app.utils.offline_guard import validate_runtime_config


router = APIRouter(prefix="/settings", tags=["settings"])


def _deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


@router.get("")
def read_settings() -> dict:
    settings = get_settings()
    return settings.model_dump()


@router.post("/update")
def update_settings(payload: SettingsUpdate) -> dict:
    settings = get_settings()
    merged = _deep_merge(settings.model_dump(), payload.model_dump(exclude_unset=True))
    updated = AppSettings.model_validate(merged)
    try:
        validate_runtime_config(updated)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    updated.config_path.write_text(
        yaml.safe_dump(updated.model_dump(), sort_keys=False),
        encoding="utf-8",
    )
    reload_settings()
    return {"status": "updated", "settings": get_settings().model_dump()}


@router.get("/models")
def read_models() -> dict:
    return list_local_models(get_settings())


@router.post("/test-ollama")
def test_ollama() -> dict:
    settings = get_settings()
    status = check_ollama_status(settings)
    model_test = test_model(settings.ollama.llm_model, settings)
    return {"ollama": status, "model": model_test}
