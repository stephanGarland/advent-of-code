py_files := "$(git diff --name-only --diff-filter=ACMR **/*.py)"

_default:
    @just --list --unsorted

check: fmt mypy

[no-cd]
fmt *ARGS=py_files:
    uv run ruff check --select I --fix {{ ARGS }}
    uv run ruff check --fix {{ ARGS }}
    uv run ruff format {{ ARGS }}

[no-cd]
mypy *ARGS=py_files:
    uv run mypy {{ ARGS }}

# TODO: fix
run:
    uv run scripts/runner.py
    
download *ARGS:
    uv run scripts/bootstrap.py --download {{ ARGS }}

template *ARGS:
    uv run scripts/bootstrap.py --template {{ ARGS }}
