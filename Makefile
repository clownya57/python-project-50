install:
	uv sync

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=gendiff --cov-report=xml

lint:
	uv run ruff check .

check: lint test

build:
	uv build

.PHONY: install test test-coverage lint check build
