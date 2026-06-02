from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


APP_NAME = "EnterpriseOfflineAI"


class BackendConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8765


class OllamaConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 11434
    llm_model: str = "qwen2.5:7b"
    embedding_model: str = "nomic-embed-text"

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


class SecurityConfig(BaseModel):
    offline_only: bool = True
    allow_external_urls: bool = False
    telemetry_enabled: bool = False
    auto_update_enabled: bool = False


class RagConfig(BaseModel):
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 5


class StorageConfig(BaseModel):
    data_dir: str = Field(default_factory=lambda: str(default_data_dir()))


class AppSettings(BaseModel):
    backend: BackendConfig = Field(default_factory=BackendConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    rag: RagConfig = Field(default_factory=RagConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)

    @property
    def data_dir(self) -> Path:
        return Path(os.path.expandvars(self.storage.data_dir)).expanduser()

    @property
    def config_path(self) -> Path:
        return self.data_dir / "config.yaml"

    @property
    def database_path(self) -> Path:
        return self.data_dir / "app.db"


def default_data_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / APP_NAME
    return Path.home() / "AppData" / "Local" / APP_NAME


def default_settings() -> AppSettings:
    return AppSettings()


def ensure_data_directories(settings: AppSettings) -> None:
    for folder in (
        settings.data_dir,
        settings.data_dir / "uploads",
        settings.data_dir / "processed",
        settings.data_dir / "vector_db",
        settings.data_dir / "exports",
        settings.data_dir / "logs",
        settings.data_dir / "backups",
    ):
        folder.mkdir(parents=True, exist_ok=True)


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def write_default_config(settings: AppSettings) -> None:
    settings.config_path.write_text(
        yaml.safe_dump(settings.model_dump(), sort_keys=False),
        encoding="utf-8",
    )


def load_settings() -> AppSettings:
    settings = default_settings()
    ensure_data_directories(settings)
    if not settings.config_path.exists():
        write_default_config(settings)
        return settings

    loaded = yaml.safe_load(settings.config_path.read_text(encoding="utf-8")) or {}
    merged = _deep_merge(settings.model_dump(), loaded)
    resolved = AppSettings.model_validate(merged)
    ensure_data_directories(resolved)
    return resolved


@lru_cache
def get_settings() -> AppSettings:
    return load_settings()


def reload_settings() -> AppSettings:
    get_settings.cache_clear()
    return get_settings()
