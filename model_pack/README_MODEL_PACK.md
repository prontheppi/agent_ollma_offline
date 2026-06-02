# Offline Model Pack

Models are not downloaded during runtime. Prepare and install the model pack separately according to the organization's offline deployment process.

Recommended models:

- LLM: `qwen2.5:7b`
- Embeddings: `nomic-embed-text`

Example preparation on a staging machine with internet access:

```powershell
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

Do not run model pulls from the installed offline application.
