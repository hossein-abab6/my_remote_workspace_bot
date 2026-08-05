from __future__ import annotations

from app.models import AgentSettings, AppSettings

from .base import AgentAdapter


def create_adapter(settings: AgentSettings) -> AgentAdapter:
    if settings.provider == "claude":
        from .claude import ClaudeAdapter

        return ClaudeAdapter(settings)
    if settings.provider == "codex":
        from .codex import CodexAdapter

        return CodexAdapter(settings)
    if settings.provider == "gemini":
        from .gemini import GeminiAdapter

        return GeminiAdapter(settings)
    from .custom_cli import CustomCliAdapter

    return CustomCliAdapter(settings)


def get_default_agent(settings: AppSettings) -> AgentSettings:
    if not settings.agents:
        return AgentSettings(is_default=True)
    return next((agent for agent in settings.agents if agent.is_default), settings.agents[0])


def get_agent_by_provider(settings: AppSettings, provider: str) -> AgentSettings | None:
    return next((agent for agent in settings.agents if agent.provider == provider), None)
