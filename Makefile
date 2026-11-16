# general-ai-api: the same commands as every DX repo (`make help`).
# `make setup` once, then `make dev` runs the API on this machine. To run the
# whole DX stack, in Docker or not, use infra.dx.

PYTHON ?= 3.11
VENV := .venv
IMAGE ?= dx-ai-api:local

.DEFAULT_GOAL := help
.PHONY: help setup dev build lint

help: ## List the commands
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  %-10s %s\n", $$1, $$2}'

setup: ## Create a Python 3.11 virtualenv in .venv with the dependencies, create .env
	@if command -v uv >/dev/null; then \
	  [ -d $(VENV) ] || uv venv --python $(PYTHON) $(VENV); \
	  uv pip install --python $(VENV)/bin/python -r requirements.txt; \
	else \
	  [ -d $(VENV) ] || python$(PYTHON) -m venv $(VENV); \
	  $(VENV)/bin/pip install -r requirements.txt; \
	fi
	@[ -f .env ] || { cp .env.example .env && echo "Created .env from .env.example"; }

# dx.server calls the AI API on port 5000. On macOS, turn off the AirPlay
# Receiver (System Settings > General > AirDrop & Handoff) if it holds that port.
dev: ## Run the API on http://localhost:5000, reloading on changes
	@[ -x $(VENV)/bin/flask ] || { echo "No virtualenv yet: run make setup." >&2; exit 1; }
	$(VENV)/bin/flask run --port 5000 --debug

build: ## Build the Docker image, as CI does
	docker build -t $(IMAGE) .

lint: ## Check code style
	$(VENV)/bin/flake8 .
