from __future__ import annotations

import json
from pathlib import Path

from app.validation import resolve_executable

from .base import AgentAdapter, AgentReply
from .utils import extract_dot_path, parse_json_lines, run_process, substitute_args


class CustomCliAdapter(AgentAdapter):
    async def send(
        self,
        prompt: str,
        project_path: Path,
        mode: str,
        external_session_id: str | None = None,
    ) -> AgentReply:
        custom = self.settings.custom
        executable = resolve_executable(custom.executable, custom.executable)
        if not executable:
            raise RuntimeError("Custom CLI executable was not found.")
        template = custom.resume_session_args if external_session_id else custom.new_session_args
        args = substitute_args(template, prompt, external_session_id)
        environment = dict(self.settings.extra_environment)
        environment.update(custom.environment)
        code, stdout, stderr = await run_process(executable, args, project_path, environment)
        if code != 0:
            raise RuntimeError(stderr.strip() or stdout.strip() or f"Custom agent exited with code {code}.")

        response = stdout.strip()
        session_id = external_session_id
        if custom.output_format == "json":
            value = json.loads(stdout)
            extracted = extract_dot_path(value, custom.response_json_path)
            session = extract_dot_path(value, custom.session_id_json_path)
            response = str(extracted if extracted is not None else value)
            if session is not None:
                session_id = str(session)
        elif custom.output_format == "jsonl":
            rows = parse_json_lines(stdout)
            if rows:
                last = rows[-1]
                extracted = extract_dot_path(last, custom.response_json_path)
                session = extract_dot_path(last, custom.session_id_json_path)
                response = str(extracted if extracted is not None else last)
                if session is not None:
                    session_id = str(session)
        return AgentReply(text=response or "Custom agent completed without a textual response.", external_session_id=session_id)
