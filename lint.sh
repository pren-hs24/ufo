cd src
uv run ruff format
uv run ruff check --fix
uv run mypy . --strict
uv run pylint *.py */ --recursive=y --rcfile=../.pylintrc