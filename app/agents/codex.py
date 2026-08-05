from __future__ import annotations

from pathlib import Path

from app.validation import resolve_executable

from .base import AgentAdapter, AgentReply
from .utils import parse_json_lines, run_process


class CodexAdapter(AgentAdapter):
    async def send(
        self,
        prompt: str,
        project_path: Path,
        mode: str,
        external_session_id: str | None = None,
    ) -> AgentReply:
        executable = resolve_executable(self.settings.executable, "codex")
        if not executable:
            raise RuntimeError("Codex CLI executable was not found.")
        args = ["exec", "--json", "--sandbox", mode, "--skip-git-repo-check"]
        if self.settings.model:
            args.extend(["--model", self.settings.model])
        if external_session_id:
            args.extend(["resume", external_session_id, prompt])
        else:
            args.append(prompt)
        code, stdout, stderr = await run_process(
            executable, args, project_path, self.settings.extra_environment
        )
        if code != 0:
            raise RuntimeError(stderr.strip() or stdout.strip() or f"Codex exited with code {code}.")

        session_id = external_session_id
        responses: list[str] = []
        for event in parse_json_lines(stdout):
            if event.get("type") == "thread.started":
                session_id = event.get("thread_id") or session_id
            item = event.get("item")
            if event.get("type") == "item.completed" and isinstance(item, dict):
                if item.get("type") == "agent_message" and item.get("text"):
                    responses.append(str(item["text"]))
        if not responses:
            responses.append(stdout.strip())
        return AgentReply(text="\n".join(responses).strip(), external_session_id=session_id)
