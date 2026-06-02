# EnterpriseOfflineAI

EnterpriseOfflineAI is an offline-first Windows desktop AI document assistant. Phase 1 implements the local backend foundation only: FastAPI, SQLite initialization, local settings, an offline guard, and an Ollama availability check against `127.0.0.1:11434`.

## Phase 1 Scope

- FastAPI backend served only on `127.0.0.1:8765`
- `GET /health`
- `GET /settings`
- `POST /settings/update`
- `GET /settings/models`
- `POST /settings/test-ollama`
- SQLite schema creation in the local data directory
- Local `config.yaml` creation under `%LOCALAPPDATA%\EnterpriseOfflineAI`
- Local-only URL validation and fail-closed security checks
- Ollama status check using localhost only

## Offline Requirement

This project must not call cloud AI APIs, external model providers, telemetry, analytics, crash reporting, update checks, or any external server during operation. All runtime services must use `127.0.0.1` or local files only.

## Development

From `backend/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
python run_backend.py
```

The backend refuses to bind to `0.0.0.0` or LAN addresses.

## Health Check

```powershell
Invoke-RestMethod http://127.0.0.1:8765/health
```

Ollama should be installed separately and running locally before AI features are used. Phase 1 only checks status; it does not pull or download models.
