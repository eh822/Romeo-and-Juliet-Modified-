
run_all:
	poetry run moo

install:
	poetry install

format:
	poetry run ruff format main/ tests/

lint:
	poetry run ruff check main/ tests/


all: format lint