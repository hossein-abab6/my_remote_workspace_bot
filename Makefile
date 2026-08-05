.PHONY: install install-dev run test lint check

install:
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install -r requirements-dev.txt

run:
	python run.py

test:
	python -m pytest

lint:
	ruff check .

check: lint test
	python scripts/check_repo.py
