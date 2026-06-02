from pydantic import BaseModel

from app.config import BackendConfig, OllamaConfig, RagConfig, SecurityConfig, StorageConfig


class SettingsUpdate(BaseModel):
    backend: BackendConfig | None = None
    ollama: OllamaConfig | None = None
    security: SecurityConfig | None = None
    rag: RagConfig | None = None
    storage: StorageConfig | None = None
