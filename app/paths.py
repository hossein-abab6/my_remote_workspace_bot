from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def data_dir() -> Path:
    raw = os.getenv("MRWB_DATA_DIR", "./data")
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def settings_path() -> Path:
    return data_dir() / "settings.json"


def database_path() -> Path:
    return data_dir() / "workspace_bot.db"


def telegram_proxy() -> str | None:
    """Proxy URL used for every call to api.telegram.org.

    Telegram is unreachable from some networks; without a proxy the bot fails to
    start with a connect timeout. Accepts http://, socks5:// or socks5h:// URLs.
    """
    for name in ("MRWB_TELEGRAM_PROXY", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy"):
        value = os.getenv(name, "").strip()
        if value:
            return value
    return None


def logs_dir() -> Path:
    path = PROJECT_ROOT / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path
