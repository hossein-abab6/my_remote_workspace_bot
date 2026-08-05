from __future__ import annotations

import json
import re
from pathlib import Path

from app.validation import resolve_executable

from .base import AgentAdapter, AgentReply
from .utils import extract_dot_path, run_process

UUID_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
)


class GeminiAdapter(AgentAdapter):
    async def _list_session_ids(self, executable: str, project_path: Path) -> set[str]:
        code, stdout, _ = await run_process(
            executable,
            ["--list-sessions"],
            project_path,
            self.settings.extra_environment,
            timeout=60,
        )
        if code != 0:
            return set()
        return set(UUID_PATTERN.findall(stdout))

    async def send(
        self,
        prompt: str,
        project_path: Path,
        mode: str,
        external_session_id: str | None = None,
    ) -> AgentReply:
        executable = resolve_executable(self.settings.executable, "gemini")
        if not executable:
            raise RuntimeError("Gemini CLI executable was not found.")

        before_ids = set()
        if not external_session_id:
            before_ids = await self._list_session_ids(executable, project_path)

        args = ["-p", prompt, "--output-format", "json", "--approval-mode", mode]
        if external_session_id:
            args.extend(["--resume", external_session_id])
        if self.settings.model:
            args.extend(["--model", self.settings.model])
        code, stdout, stderr = await run_process(
            executable, args, project_path, self.settings.extra_environment
        )
        if code != 0:
            raise RuntimeError(stderr.strip() or stdout.strip() or f"Gemini exited with code {code}.")

        text = stdout.strip()
        session_id = external_session_id
        try:
            value = json.loads(stdout)
            if isinstance(value, dict):
                nested_session = value.get("session")
                session_id = str(
                    value.get("session_id")
                    or value.get("sessionId")
                    or (nested_session.get("id") if isinstance(nested_session, dict) else "")
                    or session_id
                    or ""
                ) or None
                result = (
                    value.get("response")
                    or value.get("result")
                    or value.get("text")
                    or extract_dot_path(value, "message.content")
                )
                if result:
                    text = str(result)
        except json.JSONDecodeError:
            pass

        if not session_id and not external_session_id:
            after_ids = await self._list_session_ids(executable, project_path)
            new_ids = after_ids - before_ids
            if len(new_ids) == 1:
                session_id = new_ids.pop()

        return AgentReply(
            text=text or "Gemini completed without a textual response.",
            external_session_id=session_id,
        )
