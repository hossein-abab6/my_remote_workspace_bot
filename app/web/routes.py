from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from telegram import Bot
from telegram.request import HTTPXRequest

from app.models import SettingsPayload
from app.paths import PROJECT_ROOT, telegram_proxy
from app.runtime import describe_start_failure
from app.settings import load_settings, save_settings, to_public
from app.validation import (
    allowed_modes,
    validate_agent_runtime,
    validate_agent_settings,
    validate_payload,
    validate_projects_root,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "app" / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/api/settings")
async def get_settings() -> dict:
    settings = load_settings()
    return to_public(settings).model_dump()


PROVIDER_LABELS = {
    "claude": "Claude Code",
    "codex": "OpenAI Codex CLI",
    "gemini": "Gemini CLI",
    "custom": "Custom CLI adapter",
}


@router.get("/api/meta")
async def get_meta() -> dict:
    # The provider catalogue is static: it lists what can be configured, not what is
    # configured. Deriving it from saved agents leaves it empty on first run.
    return {
        "providers": [
            {
                "value": provider,
                "label": label,
                "modes": allowed_modes(provider),
            }
            for provider, label in PROVIDER_LABELS.items()
        ],
        "transportProviders": [
            {
                "value": "telegram",
                "label": "Telegram",
                "description": "Included transport. The codebase is structured so more transports can be added later.",
            }
        ],
    }


@router.get("/api/status")
async def get_status(request: Request) -> dict:
    runtime = request.app.state.runtime
    return {
        "configured": runtime.status.configured,
        "botRunning": runtime.status.bot_running,
        "agentProvider": runtime.status.agent_provider,
        "agentName": runtime.status.agent_name,
        "error": runtime.status.error,
    }


@router.post("/api/validate/root")
async def validate_root(payload: dict) -> dict:
    try:
        path = validate_projects_root(str(payload.get("projects_root", "")))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"ok": True, "message": f"Directory exists and is writable: {path}"}


@router.post("/api/validate/telegram")
async def validate_telegram(payload: dict) -> dict:
    token = str(payload.get("bot_token", "")).strip()
    keep_existing = bool(payload.get("keep_existing_bot_token"))
    if not token and keep_existing:
        token = load_settings().telegram.bot_token
    if not token:
        raise HTTPException(status_code=422, detail="Enter a bot token first.")
    proxy = telegram_proxy()
    try:
        bot = Bot(token, request=HTTPXRequest(proxy=proxy) if proxy else None)
        await bot.initialize()
        try:
            info = await bot.get_me()
        finally:
            await bot.shutdown()
    except Exception as exc:
        raise HTTPException(status_code=422, detail=describe_start_failure(exc)) from exc
    return {
        "ok": True,
        "message": f"Connected to @{info.username or info.first_name} (bot ID {info.id}).",
    }


@router.post("/api/validate/agent")
async def validate_agent(payload: SettingsPayload) -> dict:
    if not payload.agents:
        raise HTTPException(status_code=422, detail="Configure at least one agent.")
    messages: list[str] = []
    for agent in payload.agents:
        try:
            validate_projects_root(payload.projects_root)
            validate_agent_settings(agent)
            ok, message = await validate_agent_runtime(agent)
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=422, detail=f"{agent.display_name}: {exc}") from exc
        if not ok:
            raise HTTPException(status_code=422, detail=f"{agent.display_name}: {message}")
        messages.append(f"{agent.display_name}: {message}")
    return {"ok": True, "message": " | ".join(messages)}


@router.post("/api/settings")
async def update_settings(payload: SettingsPayload, request: Request) -> dict:
    existing = load_settings()
    try:
        validate_payload(payload, existing)
        settings = save_settings(payload)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    runtime = request.app.state.runtime
    try:
        await runtime.restart_bot()
        restart_message = (
            "Settings saved and Telegram bot restarted."
            if settings.telegram.enabled
            else "Settings saved. Telegram bot is disabled."
        )
    except Exception as exc:
        restart_message = f"Settings were saved, but the bot could not start: {exc}"

    success = (not settings.telegram.enabled) or runtime.status.bot_running
    return {
        "ok": success,
        "message": restart_message,
        "settings": to_public(settings).model_dump(),
        "status": {
            "configured": runtime.status.configured,
            "botRunning": runtime.status.bot_running,
            "agentProvider": runtime.status.agent_provider,
            "agentName": runtime.status.agent_name,
            "error": runtime.status.error,
        },
    }
