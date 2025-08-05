
run_all:
	poetry run python3 romeomodified.py

install:
	poetry install --no-root

format:
	poetry run ruff format romeomodified.py

lint:
	poetry run ruff check romeomodified.py


all: format lint