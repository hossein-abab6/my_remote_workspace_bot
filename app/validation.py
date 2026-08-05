from __future__ import annotations

import asyncio
import os
import re
import shutil
from pathlib import Path

from .models import AgentSettings, AppSettings, SettingsPayload

CLAUDE_MODES = ["default", "acceptEdits", "plan", "dontAsk", "bypassPermissions", "auto"]
CODEX_MODES = ["read-only", "workspace-write", "danger-full-access"]
GEMINI_MODES = ["default", "auto_edit", "plan", "yolo"]
CUSTOM_MODES = ["default"]


def allowed_modes(provider: str) -> list[str]:
    return {
        "claude": CLAUDE_MODES,
        "codex": CODEX_MODES,
        "gemini": GEMINI_MODES,
        "custom": CUSTOM_MODES,
    }.get(provider, [])


def resolve_executable(value: str, default_name: str) -> str | None:
    candidate = value.strip() or default_name
    expanded = str(Path(candidate).expanduser())
    if os.path.sep in expanded or (os.path.altsep and os.path.altsep in expanded):
        path = Path(expanded)
        return str(path.resolve()) if path.exists() and path.is_file() else None
    return shutil.which(candidate)


def validate_projects_root(raw: str) -> Path:
    if not raw.strip():
        raise ValueError("Projects root is required.")
    path = Path(raw).expanduser()
    if not path.exists():
        raise ValueError(f"Projects root does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Projects root is not a directory: {path}")
    try:
        probe = path / ".mrwb_write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        raise ValueError(f"Projects root is not writable: {exc}") from exc
    return path.resolve()


def validate_agent_settings(agent: AgentSettings) -> None:
    modes = allowed_modes(agent.provider)
    if agent.default_mode not in modes:
        raise ValueError(
            f"Mode '{agent.default_mode}' is not valid for {agent.provider}. "
            f"Allowed modes: {', '.join(modes)}"
        )
    if agent.provider == "custom" and not agent.custom.executable.strip():
        raise ValueError("Custom CLI executable is required.")


def validate_payload(payload: SettingsPayload, existing: AppSettings | None = None) -> None:
    validate_projects_root(payload.projects_root)
    if payload.telegram_enabled:
        token = payload.bot_token.strip()
        if payload.keep_existing_bot_token and not token and existing:
            token = existing.telegram.bot_token
        if not token:
            raise ValueError("Telegram bot token is required while Telegram is enabled.")
        if not re.fullmatch(r"\d{6,15}:[A-Za-z0-9_-]{20,}", token):
            raise ValueError("Telegram token format is invalid. Copy the complete token from @BotFather.")
        if not payload.allowed_user_ids:
            raise ValueError("Add at least one allowed Telegram user ID.")
    if not payload.agents:
        raise ValueError("Configure at least one agent.")
    seen: set[str] = set()
    for agent in payload.agents:
        validate_agent_settings(agent)
        if agent.provider in seen:
            raise ValueError(
                f"Provider '{agent.provider}' is configured twice. Each provider can be used once."
            )
        seen.add(agent.provider)


async def run_version_command(executable: str, args: list[str]) -> tuple[bool, str]:
    try:
        process = await asyncio.create_subprocess_exec(
            executable,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15)
    except FileNotFoundError:
        return False, f"Executable not found: {executable}"
    except asyncio.TimeoutError:
        return False, "Version check timed out after 15 seconds."
    except OSError as exc:
        return False, f"Cannot start executable: {exc}"
    text = (stdout + stderr).decode("utf-8", errors="replace").strip()
    if process.returncode != 0:
        return False, text or f"Process exited with code {process.returncode}."
    return True, text[:1000] or "Executable started successfully."


async def validate_agent_runtime(agent: AgentSettings) -> tuple[bool, str]:
    if agent.provider == "claude":
        executable = resolve_executable(agent.executable, "claude")
        if executable:
            return await run_version_command(executable, ["--version"])
        try:
            import claude_agent_sdk  # noqa: F401
        except ImportError:
            return False, "Claude Agent SDK is not installed and the claude executable was not found."
        return True, "Claude Agent SDK is installed. The CLI will be resolved by the SDK at runtime."

    if agent.provider == "codex":
        executable = resolve_executable(agent.executable, "codex")
        if not executable:
            return False, "Codex CLI was not found. Install it or provide its executable path."
        return await run_version_command(executable, ["--version"])

    if agent.provider == "gemini":
        executable = resolve_executable(agent.executable, "gemini")
        if not executable:
            return False, "Gemini CLI was not found. Install it or provide its executable path."
        return await run_version_command(executable, ["--version"])

    executable = resolve_executable(agent.custom.executable, agent.custom.executable)
    if not executable:
        return False, "Custom CLI executable was not found."
    return await run_version_command(executable, agent.custom.version_args)
