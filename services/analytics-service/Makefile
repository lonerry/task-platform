.PHONY: all

SHELL=/bin/bash -e

.DEFAULT_GOAL := help


help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint: ## Lint with flake8 and type-check with mypy
	uvx flake8 ./
	uvx mypy ./src

format: ## Format with autopep8, isort, and black
	uvx autopep8 --aggressive --experimental -r -i ./
	uvx isort ./
	uvx black --fast ./ --skip-string-normalization

pre-commit-enable: ## Enable pre-commit
	uvx pre-commit install

pre-commit-disable: ## Disable pre-commit
	uvx pre-commit uninstall

run: ## Run project with uv
	uv run python src/main.py

build: ## build dev images
	./build.sh

up: ## start docker dev environment
	docker-compose up -d
	docker-compose ps

down: ## stop docker dev environment
	docker-compose down

purge: ## stop docker dev environment and remove orphans and volumes
	docker-compose down --volumes --remove-orphans

test:  ## run pytest
	pytest tests

logs:  ## show logs for app container
	docker-compose logs -f web

precommit-check: ## used precommit for all files
	pre-commit run --all-files
