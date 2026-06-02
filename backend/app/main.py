from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, settings
from app.config import get_settings
from app.database.init_db import initialize_database
from app.utils.offline_guard import validate_runtime_config


def create_app() -> FastAPI:
    app_settings = get_settings()
    validate_runtime_config(app_settings)
    initialize_database(app_settings)

    app = FastAPI(
        title="EnterpriseOfflineAI Backend",
        version="0.1.0-phase1",
        docs_url="/docs",
        redoc_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:1420",
            "http://localhost:1420",
            "tauri://localhost",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.include_router(health.router)
    app.include_router(settings.router)
    return app


app = create_app()
