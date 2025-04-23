.PHONY: format lint dev-lint

GIT_ROOT ?= $(shell git rev-parse --show-toplevel)

dev-lint:
	black .
	isort .
	ruff check . --fix
	# mypy .
	pylint src/. evals/. --max-line-length 120 --disable=R,C,I

lint:
	black . --check
	isort . --check-only
	ruff check .
	# mypy .
	pylint src/. evals/. --max-line-length 120 --disable=R,C,I
