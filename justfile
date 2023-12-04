py_files := "$(git diff --name-only --diff-filter=ACMR *.py)"

fmt:
    poetry run black {{ py_files }}
    poetry run isort {{ py_files }}
    poetry run flakeheaven lint {{ py_files }}

test:
    poetry run mypy {{ py_files }}
