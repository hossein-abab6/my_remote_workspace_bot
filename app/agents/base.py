from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from app.models import AgentSettings


@dataclass(slots=True)
class AgentReply:
    text: str
    external_session_id: str | None = None


class AgentAdapter(ABC):
    def __init__(self, settings: AgentSettings) -> None:
        self.settings = settings

    @abstractmethod
    async def send(
        self,
        prompt: str,
        project_path: Path,
        mode: str,
        external_session_id: str | None = None,
    ) -> AgentReply:
        raise NotImplementedError
