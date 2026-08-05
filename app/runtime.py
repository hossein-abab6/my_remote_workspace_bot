from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from .database import initialize_database
from .paths import telegram_proxy
from .settings import load_settings

logger = logging.getLogger(__name__)


def describe_start_failure(exc: Exception) -> str:
    """Turn a bare 'Timed out' into something a user can act on."""
    from telegram.error import InvalidToken, NetworkError

    if isinstance(exc, InvalidToken):
        return "Telegram rejected the bot token. Re-copy it from @BotFather."
    if isinstance(exc, NetworkError):
        if telegram_proxy():
            return (
                f"Could not reach api.telegram.org through the configured proxy ({exc}). "
                "Check that the proxy is running and reachable."
            )
        return (
            f"Could not reach api.telegram.org ({exc}). If Telegram is blocked on this "
            "network, set MRWB_TELEGRAM_PROXY in .env to a working proxy URL and restart."
        )
    return str(exc)


@dataclass(slots=True)
class RuntimeStatus:
    configured: bool = False
    bot_running: bool = False
    agent_provider: str = ""
    agent_name: str = ""
    error: str = ""


class ApplicationRuntime:
    def __init__(self) -> None:
        self.telegram_service = None
        self._lock = asyncio.Lock()
        self.status = RuntimeStatus()

    async def start(self) -> None:
        initialize_database()
        settings = load_settings()
        self.status.configured = settings.configured
        # Get the first agent from the list if available, otherwise use default
        agent = settings.agents[0] if settings.agents else None
        self.status.agent_provider = agent.provider if agent and settings.configured else ""
        self.status.agent_name = agent.display_name if agent and settings.configured else ""
        if settings.configured and settings.telegram.enabled:
            await self.start_bot()

    async def start_bot(self) -> None:
        async with self._lock:
            await self._stop_bot_unlocked()
            settings = load_settings()
            self.status.configured = settings.configured
            # Get the first agent from the list if available, otherwise use default
            agent = settings.agents[0] if settings.agents else None
            self.status.agent_provider = agent.provider if agent and settings.configured else ""
            self.status.agent_name = agent.display_name if agent and settings.configured else ""
            self.status.error = ""
            if not settings.configured or not settings.telegram.enabled:
                self.status.bot_running = False
                return
            from .telegram.service import TelegramService

            service = TelegramService(settings)
            try:
                await service.start()
            except Exception as exc:
                logger.exception("Telegram bot failed to start")
                self.status.bot_running = False
                self.status.error = describe_start_failure(exc)
                raise RuntimeError(self.status.error) from exc
            self.telegram_service = service
            self.status.bot_running = True
            self.status.configured = True
            # Get the first agent from the list if available
            agent = settings.agents[0] if settings.agents else None
            self.status.agent_provider = agent.provider if agent else ""
            self.status.agent_name = agent.display_name if agent else ""
            self.status.error = ""

    async def _stop_bot_unlocked(self) -> None:
        if self.telegram_service is not None:
            try:
                await self.telegram_service.stop()
            finally:
                self.telegram_service = None
                self.status.bot_running = False

    async def stop_bot(self) -> None:
        async with self._lock:
            await self._stop_bot_unlocked()

    async def restart_bot(self) -> None:
        await self.start_bot()

    async def shutdown(self) -> None:
        await self.stop_bot()
