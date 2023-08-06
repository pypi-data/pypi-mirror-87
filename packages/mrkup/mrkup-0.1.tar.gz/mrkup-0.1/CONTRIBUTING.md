# Contributing

Pull requests are welcome!

You can also help by opening an issue if you find any bug.

This project uses the following for development:

| Package         | Purpose              |
| -------         | -------              |
| pytest          | Testing              |
| vulture         | Dead code detection  |
| mypy            | Static type checking |
| pylint & flake8 | Linting              |
| coverage        | Test coverage        |
| tox             | Test automation      |

Use the following command to install them.

    pip install -r requirements-dev.txt

## Docstring style

Follow [Google style guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for docstrings.

## Tests (pytest)

Make sure to add tests for any new piece of code using pytest.

    pytest

## Dead code detection (vulture)

Vulture to check for dead code.

    tox -e vulture

## Static type checking (mypy)

Use type annotations for every function definition and apply mypy for static type checking.

    tox -e mypy

## Linting (pylint and flake8)

Use both pylint and flake8 for linting.

    tox -e pylint,flake8

## Test coverage (coverage)

Ensure proper test coverage with coverage.py

    tox -e coverage

## All checks

Run all checks with

    tox
