# Contributing

Thank you for improving `my_remote_workspace_bot`.

## Development setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
ruff check .
```

## Pull requests

1. Open an issue for large behavioral changes.
2. Keep transport and agent integrations behind their existing interfaces.
3. Add or update tests.
4. Do not commit tokens, local paths, databases, transcripts, logs, or generated agent caches.
5. Update both README files when user-facing setup changes.
6. Use clear commit messages and keep unrelated formatting changes separate.

## Adding an agent adapter

- Implement `AgentAdapter.send` in `app/agents/`.
- Add provider-specific validation and modes in `app/validation.py`.
- Register the adapter in `app/agents/registry.py`.
- Add UI fields only when generic fields cannot represent the integration.
- Document authentication, non-interactive usage, resume behavior, and permission semantics.

## Adding a transport

Telegram is currently the bundled transport. A new transport should own only message delivery and UI interaction; workspace and agent logic should remain reusable.
