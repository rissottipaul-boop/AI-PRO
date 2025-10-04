PY=python
PKG=autonomous_dev
SRC=src/$(PKG)

.PHONY: install lint test format type all pre-commit

install:
	$(PY) -m pip install --upgrade pip
	pip install .[dev]

lint:
	ruff check .
	ruff format --check .
	mypy $(SRC)

format:
	ruff check --fix . || true
	ruff format .
	black .

Type:
	mypy $(SRC)

test:
	pytest -q

all: lint test

pre-commit:
	pre-commit run --all-files
