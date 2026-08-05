from pathlib import Path

import pytest

from app.models import AgentSettings, SettingsPayload
from app.validation import allowed_modes, validate_payload


def payload(root: Path) -> SettingsPayload:
    return SettingsPayload(
        projects_root=str(root),
        telegram_enabled=True,
        bot_token="123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcd",
        allowed_user_ids=[123456789],
        agents=[
            AgentSettings(
                provider="claude",
                display_name="Claude Code",
                default_mode="acceptEdits",
                is_default=True,
            )
        ],
    )


def test_provider_modes_are_explicit() -> None:
    assert "acceptEdits" in allowed_modes("claude")
    assert "workspace-write" in allowed_modes("codex")
    assert "auto_edit" in allowed_modes("gemini")


def test_valid_payload(tmp_path: Path) -> None:
    validate_payload(payload(tmp_path))


def test_rejects_wrong_mode(tmp_path: Path) -> None:
    value = payload(tmp_path)
    value.agents[0].default_mode = "danger-full-access"
    with pytest.raises(ValueError, match="not valid"):
        validate_payload(value)


def test_rejects_missing_users(tmp_path: Path) -> None:
    value = payload(tmp_path)
    value.allowed_user_ids = []
    with pytest.raises(ValueError, match="at least one"):
        validate_payload(value)


def test_rejects_duplicate_provider(tmp_path: Path) -> None:
    value = payload(tmp_path)
    value.agents.append(
        AgentSettings(provider="claude", display_name="Claude Code 2", default_mode="plan")
    )
    with pytest.raises(ValueError, match="configured twice"):
        validate_payload(value)


def test_rejects_empty_agent_list(tmp_path: Path) -> None:
    value = payload(tmp_path)
    value.agents = []
    with pytest.raises(ValueError, match="at least one agent"):
        validate_payload(value)
