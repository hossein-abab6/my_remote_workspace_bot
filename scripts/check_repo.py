from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

required = [
    "README.md",
    "README.fa.md",
    "LICENSE",
    ".gitignore",
    "pyproject.toml",
    "requirements.txt",
    "app/main.py",
    "app/templates/index.html",
    "data/.gitkeep",
    "logs/.gitkeep",
]

missing = [item for item in required if not (ROOT / item).exists()]
if missing:
    raise SystemExit("Missing required repository files: " + ", ".join(missing))

subprocess.run(["python", "-m", "compileall", "-q", "app", "run.py"], cwd=ROOT, check=True)
print("Repository structure and Python syntax checks passed.")
