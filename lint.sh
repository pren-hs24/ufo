cd src
python3 -m ruff format
python3 -m ruff check --fix
python3 -m mypy . --strict
python3 -m pylint *.py */ --recursive=y --rcfile=../.pylintrc