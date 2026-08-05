from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import List, Optional

from .models import AppSettings, PublicSettings, SettingsPayload, TelegramSettings, AgentSettings
from .paths import settings_path

_lock = threading.RLock()


def migrate_raw_settings(raw: dict) -> dict:
    """Upgrade a settings document written by the single-agent schema.

    Older files stored one `agent` object. Without this the key is silently
    dropped, `agents` ends up empty, and every agent lookup fails.
    """
    if isinstance(raw.get("agent"), dict) and not raw.get("agents"):
        agent = dict(raw["agent"])
        agent["is_default"] = True
        raw["agents"] = [agent]
    raw.pop("agent", None)
    return raw


def load_settings() -> AppSettings:
    path = settings_path()
    if not path.exists():
        return AppSettings()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Cannot read local settings file: {exc}") from exc
    if not isinstance(raw, dict):
        raise RuntimeError("Local settings file must contain a JSON object.")
    try:
        return AppSettings.model_validate(migrate_raw_settings(raw))
    except Exception as exc:
        raise RuntimeError(f"Cannot read local settings file: {exc}") from exc


def save_settings(payload: SettingsPayload) -> AppSettings:
    with _lock:
        existing = load_settings()
        token = payload.bot_token.strip()
        if payload.keep_existing_bot_token and not token:
            token = existing.telegram.bot_token

        # Exactly one agent must carry the default flag: it is the fallback used by
        # every Telegram user who has not picked an agent yet.
        agents = payload.agents or [
            AgentSettings(provider="claude", display_name="Claude Code")
        ]
        default_index = next(
            (index for index, agent in enumerate(agents) if agent.is_default), 0
        )
        for index, agent in enumerate(agents):
            agent.is_default = index == default_index

        settings = AppSettings(
            configured=True,
            projects_root=str(Path(payload.projects_root).expanduser().resolve()),
            transport=payload.transport,
            telegram=TelegramSettings(
                enabled=payload.telegram_enabled,
                bot_token=token,
                allowed_user_ids=payload.allowed_user_ids,
            ),
            agents=agents,
            folder_page_size=payload.folder_page_size,
            session_page_size=payload.session_page_size,
            history_page_size=payload.history_page_size,
        )
        path = settings_path()
        temp = path.with_suffix(".json.tmp")
        temp.write_text(
            json.dumps(settings.model_dump(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp.replace(path)
        return settings


def to_public(settings: AppSettings) -> PublicSettings:
    token = settings.telegram.bot_token
    if token:
        token_masked = f"{token[:6]}…{token[-4:]}"
    else:
        token_masked = ""
    return PublicSettings(
        configured=settings.configured,
        projects_root=settings.projects_root,
        transport=settings.transport,
        telegram_enabled=settings.telegram.enabled,
        bot_token_masked=token_masked,
        allowed_user_ids=settings.telegram.allowed_user_ids,
        agents=settings.agents,
        folder_page_size=settings.folder_page_size,
        session_page_size=settings.session_page_size,
        history_page_size=settings.history_page_size,
    )
