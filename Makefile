SHELL := /usr/bin/env bash

IMAGE := anilist
VERSION := latest

#! An ugly hack to create individual flags
ifeq ($(STRICT), 1)
	POETRY_COMMAND_FLAG =
	PIP_COMMAND_FLAG =
	SAFETY_COMMAND_FLAG =
	BANDIT_COMMAND_FLAG =
	SECRETS_COMMAND_FLAG =
	BLACK_COMMAND_FLAG =
	DARGLINT_COMMAND_FLAG =
	ISORT_COMMAND_FLAG =
	MYPY_COMMAND_FLAG =
else
	POETRY_COMMAND_FLAG = -
	PIP_COMMAND_FLAG = -
	SAFETY_COMMAND_FLAG = -
	BANDIT_COMMAND_FLAG = -
	SECRETS_COMMAND_FLAG = -
	BLACK_COMMAND_FLAG = -
	DARGLINT_COMMAND_FLAG = -
	ISORT_COMMAND_FLAG = -
	MYPY_COMMAND_FLAG = -
endif

##! Please tell me how to use `for loops` to create variables in Makefile :(
##! If you have better idea, please PR me in https://github.com/TezRomacH/python-package-template

ifeq ($(POETRY_STRICT), 1)
	POETRY_COMMAND_FLAG =
else ifeq ($(POETRY_STRICT), 0)
	POETRY_COMMAND_FLAG = -
endif

ifeq ($(PIP_STRICT), 1)
	PIP_COMMAND_FLAG =
else ifeq ($(PIP_STRICT), 0)
	PIP_COMMAND_FLAG = -
endif

ifeq ($(SAFETY_STRICT), 1)
	SAFETY_COMMAND_FLAG =
else ifeq ($SAFETY_STRICT), 0)
	SAFETY_COMMAND_FLAG = -
endif

ifeq ($(BANDIT_STRICT), 1)
	BANDIT_COMMAND_FLAG =
else ifeq ($(BANDIT_STRICT), 0)
	BANDIT_COMMAND_FLAG = -
endif

ifeq ($(SECRETS_STRICT), 1)
	SECRETS_COMMAND_FLAG =
else ifeq ($(SECRETS_STRICT), 0)
	SECRETS_COMMAND_FLAG = -
endif

ifeq ($(BLACK_STRICT), 1)
	BLACK_COMMAND_FLAG =
else ifeq ($(BLACK_STRICT), 0)
	BLACK_COMMAND_FLAG = -
endif

ifeq ($(DARGLINT_STRICT), 1)
	DARGLINT_COMMAND_FLAG =
else ifeq (DARGLINT_STRICT), 0)
	DARGLINT_COMMAND_FLAG = -
endif

ifeq ($(ISORT_STRICT), 1)
	ISORT_COMMAND_FLAG =
else ifeq ($(ISORT_STRICT), 0)
	ISORT_COMMAND_FLAG = -
endif


ifeq ($(MYPY_STRICT), 1)
	MYPY_COMMAND_FLAG =
else ifeq ($(MYPY_STRICT), 0)
	MYPY_COMMAND_FLAG = -
endif

#! The end of the ugly part. I'm really sorry

.PHONY: download-poetry
download-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

.PHONY: install
install:
	@poetry lock -n
	@poetry install -n
ifneq ($(NO_PRE_COMMIT), 1)
	@poetry run pre-commit install
endif

.PHONY: check-safety
check-safety:
	@echo -e "\nPoetry:"
	@$(POETRY_COMMAND_FLAG)poetry check
	@echo -e "\n\nPip Check: "
	@$(PIP_COMMAND_FLAG)poetry run pip check
	@echo -e "\n\nSafety Check: "
	@$(SAFETY_COMMAND_FLAG)poetry run safety check --full-report
	@echo -e "\n\nBandIt: "
	@$(BANDIT_COMMAND_FLAG)poetry run bandit -ll -r anilist/

.PHONY: check-style
check-style:
	@echo -e "\nBlack:"
	@$(BLACK_COMMAND_FLAG)poetry run black --config pyproject.toml --diff --check ./
	@$(DARGLINT_COMMAND_FLAG)poetry run darglint -v 2 **/*.py
	@$(ISORT_COMMAND_FLAG)poetry run isort --settings-path pyproject.toml --check-only **/*.py
	@echo -e "\nMyPy Check:"
	@$(MYPY_COMMAND_FLAG)poetry run mypy --config-file setup.cfg anilist tests/**.py
	@echo

.PHONY: codestyle
codestyle:
	@poetry run pyupgrade --py37-plus **/*.py
	@poetry run isort --settings-path pyproject.toml **/*.py
	@echo -e "\nBlack:"
	@poetry run black --config pyproject.toml ./
	@echo

.PHONY: test
test:
	@echo -e "\n\tRunning Tests:\n"
	@poetry run pytest
	@echo -e "\n"

.PHONY: test-suite
test-suite: check-safety check-style test

# Example: make docker VERSION=latest
# Example: make docker IMAGE=some_name VERSION=0.1.0
.PHONY: docker
docker:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make clean_docker VERSION=latest
# Example: make clean_docker IMAGE=some_name VERSION=0.1.0
.PHONY: clean_docker
clean_docker:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	@docker rmi -f $(IMAGE):$(VERSION)

.PHONY: clean_build
clean_build:
	@rm -rf build/

.PHONY: clean
clean: clean_build clean_docker

.PHONY: clean-cache
clean-cache:
	@rm -rf .mypy_cache/
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@rm -rf coverage.xml

.PHONY: mypy
mypy:
	@echo -e "\n\tRunning check with MyPy"
	@$(MYPY_COMMAND_FLAG)poetry run mypy --config-file setup.cfg anilist tests/**.py
