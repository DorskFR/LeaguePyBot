# Makefile
PYTHON ?= . venv/bin/activate && python
APP ?= leaguepybot

all:

setup:
	python -m venv venv
	$(PYTHON) -m pip install --upgrade pip wheel setuptools poetry
	$(PYTHON) -m poetry install

lint:
	$(PYTHON) -m autoflake -r ./$(APP) ./tests --remove-all-unused-imports --in-place
	$(PYTHON) -m isort ./$(APP) ./tests
	$(PYTHON) -m black ./$(APP) ./tests

mypy: lint
	$(PYTHON) -m mypy ./$(APP) ./tests
	$(PYTHON) -m pylint ./$(APP) ./tests

test:
	$(PYTHON) -m pytest ./tests -s -x -v $(options)

run:
	$(PYTHON) -m $(APP)

publish: lint
	$(PYTHON) -m poetry publish --repository cyberia-pypi --build

# Auto generate phony targets
.PHONY: $(shell grep --no-filename -E '^([a-zA-Z_-]|\/)+:' $(MAKEFILE_LIST) | sed 's/:.*//')
