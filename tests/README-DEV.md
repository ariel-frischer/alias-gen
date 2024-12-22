# Developer Guide

## Install
```bash
poetry install
```

## To update the version:
```bash
bumpversion minor version.py --current-version 0.5.0
```
Need to manually update version in pyproject.toml as well.

## Create a new build
```bash
poetry build
```

## Check the distribution is valid
```bash
twine check dist/*
```

## Upload test PYPI package
```bash
twine upload -r testpypi dist/*
```

## Upload actual PYPI package
```bash
twine upload dist/*
```

## Testing Locally

### Running Tests
```bash
# Install development dependencies first
poetry install

# Run all tests
pytest .

# Run specific test file
pytest tests/test_aliaser.py

# Run tests with verbose output
pytest -v .

# Run tests with coverage report
pytest --cov=alias_gen tests/
```

### Running the Built Package Locally
After building the package with `poetry build`, you can:

1. Install and run from the wheel file:
```bash
# Install the wheel file
pip install dist/*.whl

# Run the installed executable
aliaser --help
```

2. Or run directly through poetry:
```bash
# Run the package through poetry
poetry run aliaser --help

# Or activate the poetry shell first
poetry shell
aliaser --help  # Run commands in the poetry environment
```

## Bump version custom script usage
```bash
python bump_version.py patch setup.py pyproject.toml
```
Bump version parts are stucture as: major.minor.patch -> 0.6.2

## Composite Bump + Build + Upload
```bash
python bump_version.py patch setup.py pyproject.toml && rm -i -rf dist && poetry build && twine upload dist/*
```

## References

https://pypi.org/project/alias-gen/
https://test.pypi.org/project/alias-gen/
