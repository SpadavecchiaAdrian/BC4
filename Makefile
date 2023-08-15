.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean-pyc:
	echo "Clean pycache"
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

local-run: clean-pyc ## Run FastAPI locally
	echo "launch uvicorn"
	uvicorn src.main:app --reload

local-test: clean-pyc ## run test locally
	# clean
	find . -name '.pytest_cache' -exec rm -rf {} +
	pytest ./src/

docker-run: clean-pyc ## Run compose locally
	echo "Export readme"
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	echo "Running api-BC4"
	docker compose -f docker-compose.yml build
	docker compose -f docker-compose.yml up -d

docker-stop: ## Stop compose
	echo "Stoping api-BC4"
	docker compose -f docker-compose.yml stop

docker-down: ## Stop and clean compose
	echo "dropping api-BC4"
	docker compose -f docker-compose.yml -v down --remove-orphans
