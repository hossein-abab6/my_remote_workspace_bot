from __future__ import annotations

from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from .base import AgentAdapter, AgentReply


class ClaudeAdapter(AgentAdapter):
    async def send(
        self,
        prompt: str,
        project_path: Path,
        mode: str,
        external_session_id: str | None = None,
    ) -> AgentReply:
        options_kwargs: dict = {
            "cwd": str(project_path),
            "permission_mode": mode,
            "env": self.settings.extra_environment,
        }
        if self.settings.executable:
            options_kwargs["cli_path"] = self.settings.executable
        if self.settings.model:
            options_kwargs["model"] = self.settings.model
        if self.settings.max_turns:
            options_kwargs["max_turns"] = self.settings.max_turns
        if self.settings.max_budget_usd:
            options_kwargs["max_budget_usd"] = self.settings.max_budget_usd
        if external_session_id:
            options_kwargs["resume"] = external_session_id

        text_parts: list[str] = []
        result_session_id = external_session_id
        try:
            async for message in query(prompt=prompt, options=ClaudeAgentOptions(**options_kwargs)):
                if isinstance(message, ResultMessage):
                    result_session_id = message.session_id or result_session_id
                    if message.result:
                        text_parts.append(str(message.result))
        except Exception:
            # The CLI often reports the real problem (auth, quota, org policy)
            # inside the final ResultMessage.result before exiting non-zero.
            # The SDK's own exception text is a generic wrapper, so prefer
            # whatever we already collected.
            text = "\n".join(part for part in text_parts if part).strip()
            if text:
                return AgentReply(text=text, external_session_id=result_session_id)
            raise
        text = "\n".join(part for part in text_parts if part).strip()
        return AgentReply(text=text or "Claude completed without a textual response.", external_session_id=result_session_id)
