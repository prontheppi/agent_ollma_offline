from app.config import get_settings
from app.utils.offline_guard import validate_backend_host


def main() -> None:
    import uvicorn

    settings = get_settings()
    validate_backend_host(settings.backend.host)
    uvicorn.run(
        "app.main:app",
        host=settings.backend.host,
        port=settings.backend.port,
        reload=False,
        access_log=True,
    )


if __name__ == "__main__":
    main()
