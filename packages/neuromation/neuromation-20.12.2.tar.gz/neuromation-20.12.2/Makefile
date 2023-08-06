SHELL := /bin/bash

ISORT_DIRS := neuromation tests build-tools setup.py
BLACK_DIRS := $(ISORT_DIRS)
MYPY_DIRS :=  neuromation tests
FLAKE8_DIRS := $(ISORT_DIRS)
PYTEST_ARGS=

PYTEST_XDIST_NUM_THREADS ?= auto
COLOR ?= auto

.PHONY: help
.SILENT: help
help:
	echo -e "Available targets: \n\
	* Common: \n\
	- help: this help \n\
	- setup: initialize project for development \n\
	- update-deps: install.update all development dependencies \n\
	- clean: remove generated files \n\
\n\
	* Modifications and generations: \n\
	- format: format python code(isort + black) \n\
	- docs: generate docs \n\
	  example: make changelog VERSION=0.5 \n\
\n\
	* Lint (static analysis) \n\
	- lint: run linters(isort, black, flake8, mypy, lint-docs) \n\
	- lint-docs: validate generated docs \n\
	- publish-lint: lint distribution \n\
\n\
	* Tests \n\
	- test: run usual(not e2e) tests \n\
	- e2e: run e2e tests \n\
	- test-all: run all tests \n\
\n\
        * API-DOC \n\
        - api-doc: generate sphinx html docs \n\
        - api-doc-spelling: check dockumentation spelling \n\
    "

.PHONY: setup init
setup init: _init-cli-help update-deps
	rm -rf .mypy_cache
	pre-commit install

_init-cli-help:
	cp -n CLI.in.md CLI.md

.PHONY: update-deps
update-deps:
	pip install -r requirements/dev.txt
	touch .update-deps

.update-deps: $(shell find requirements -type f)
	pip install -r requirements/dev.txt
	touch .update-deps

.PHONY: .e2e
.e2e:
	COLUMNS=160 LINES=75 pytest \
	    -n ${PYTEST_XDIST_NUM_THREADS} \
		-m "e2e" \
		--cov=neuromation \
		--cov-report term-missing:skip-covered \
		--cov-report xml:coverage.xml \
		--verbose \
		--color=$(COLOR) \
		--durations 10 \
		$(PYTEST_ARGS) \
		tests

.PHONY: e2e
e2e: .update-deps .e2e

.PHONY: .e2e-jobs
.e2e-jobs:
	COLUMNS=160 LINES=75 pytest \
	    -n ${PYTEST_XDIST_NUM_THREADS} \
		-m "e2e and e2e_job" \
		--cov=neuromation \
		--cov-report term-missing:skip-covered \
		--cov-report xml:coverage.xml \
		--verbose \
		--color=$(COLOR) \
		--durations 10 \
		$(PYTEST_ARGS) \
		tests

.PHONY: e2e-jobs
e2e-jobs: .update-deps .e2e-jobs

.PHONY: e2e-sumo
.e2e-sumo:
	pytest \
	    -n ${PYTEST_XDIST_NUM_THREADS} \
		-m "e2e and not e2e_job" \
		--cov=neuromation \
		--cov-report term-missing:skip-covered \
		--cov-report xml:coverage.xml \
		--verbose \
		--color=$(COLOR) \
		--durations 10 \
		$(PYTEST_ARGS) \
		tests

.PHONY: e2e-sumo
e2e-sumo: .update-deps .e2e-sumo


.PHONY: .test
.test:
	pytest \
		-m "not e2e" \
		--cov=neuromation \
		--cov-report term-missing:skip-covered \
		--cov-report xml:coverage.xml \
		--color=$(COLOR) \
		$(PYTEST_ARGS) \
		tests

.PHONY: .test
test: .update-deps .test

.PHONY: test-all
test-all: .update-deps
	pytest \
		--cov=neuromation \
		--cov-report term-missing:skip-covered \
		--cov-report xml:coverage.xml \
		--color=$(COLOR) \
		tests


.PHONY: format fmt
format fmt:
ifdef CI_LINT_RUN
	pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files
endif


.PHONY: lint
lint: fmt
	mypy $(MYPY_DIRS)

.PHONY: publish-lint
publish-lint:
	twine check dist/*


.PHONY: clean
clean:
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	rm CLI.md

.PHONY: docs
docs:
	build-tools/cli-help-generator.py CLI.in.md CLI.md
	markdown-toc -t github -h 6 CLI.md


.PHONY: api-doc
api-doc:
	make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

.PHONY: api-doc-spelling
api-doc-spelling:
	make -C docs spelling SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"
