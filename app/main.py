from __future__ import annotations

import logging
import os
import threading
import webbrowser
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .paths import PROJECT_ROOT, logs_dir
from .runtime import ApplicationRuntime
from .web import router

load_dotenv(PROJECT_ROOT / ".env")


def configure_logging() -> None:
    level_name = os.getenv("MRWB_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    log_file = logs_dir() / "app.log"
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8")],
        force=True,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)


configure_logging()
runtime = ApplicationRuntime()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runtime = runtime
    try:
        await runtime.start()
    except Exception:
        logging.getLogger(__name__).exception("Runtime startup failed; the dashboard remains available")
    yield
    await runtime.shutdown()


app = FastAPI(
    title="my_remote_workspace_bot",
    version="0.1.1",
    description="Local dashboard and messaging gateway for workspace coding agents.",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "app" / "static")), name="static")
app.include_router(router)


def cli() -> None:
    host = os.getenv("MRWB_HOST", "127.0.0.1")
    port = int(os.getenv("MRWB_PORT", "8787"))
    open_browser = os.getenv("MRWB_OPEN_BROWSER", "true").lower() in {"1", "true", "yes", "on"}
    if open_browser:
        threading.Timer(1.2, lambda: webbrowser.open(f"http://{host}:{port}")).start()
    uvicorn.run("app.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    cli()
