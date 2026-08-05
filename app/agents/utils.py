from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any


def extract_dot_path(value: Any, path: str) -> Any:
    if not path:
        return value
    current = value
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return None
    return current


def substitute_args(args: list[str], prompt: str, session_id: str | None) -> list[str]:
    return [
        item.replace("{prompt}", prompt).replace("{session_id}", session_id or "")
        for item in args
    ]


async def run_process(
    executable: str,
    args: list[str],
    cwd: Path,
    extra_environment: dict[str, str] | None = None,
    timeout: int = 3600,
) -> tuple[int, str, str]:
    env = os.environ.copy()
    env.update(extra_environment or {})
    process = await asyncio.create_subprocess_exec(
        executable,
        *args,
        cwd=str(cwd),
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        raise RuntimeError(f"Agent process timed out after {timeout} seconds.")
    return (
        process.returncode or 0,
        stdout.decode("utf-8", errors="replace"),
        stderr.decode("utf-8", errors="replace"),
    )


def parse_json_lines(text: str) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            values.append(value)
    return values
