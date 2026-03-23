.PHONY: help install run test lint typecheck check

REPORT ?= median-coffee
FILES ?=

help:
	@echo "Available targets:"
	@echo "  make install                     Install project dependencies"
	@echo "  make run FILES='a.csv b.csv'     Run the report builder"
	@echo "  make test                        Run tests"
	@echo "  make lint                        Run ruff"
	@echo "  make typecheck                   Run mypy"
	@echo "  make check                       Run lint, typecheck and tests"

install:
	poetry install

run:
	poetry run python main.py --files $(FILES) --report $(REPORT)

test:
	poetry run pytest tests/

lint:
	poetry run ruff check .

typecheck:
	poetry run mypy .

check: lint typecheck test
