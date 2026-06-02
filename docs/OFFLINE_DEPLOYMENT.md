# Offline Deployment

## Phase 1 Checklist

1. Confirm backend host is `127.0.0.1`.
2. Confirm backend port is `8765`.
3. Confirm local `config.yaml` is created under `%LOCALAPPDATA%\EnterpriseOfflineAI`.
4. Confirm SQLite `app.db` is created locally.
5. Confirm `/health` reports offline mode enabled.
6. Confirm Ollama status uses only `http://127.0.0.1:11434`.

## Full Offline Test Checklist

1. Disable Wi-Fi.
2. Unplug LAN.
3. Open EnterpriseOfflineAI.exe.
4. Confirm backend starts.
5. Confirm Ollama is detected.
6. Login locally.
7. Upload PDF.
8. Index document.
9. Ask a question.
10. Confirm answer is generated.
11. Confirm sources are shown.
12. Confirm no outbound network calls.
13. Confirm logs are stored locally.
14. Confirm database is local.
15. Confirm uploaded files remain local.
