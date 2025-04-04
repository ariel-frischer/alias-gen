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

## Test
```bash
pytest .
```

## Running the Built Poetry Executable
After building with `poetry build`, you can run the installed package using:
```bash
poetry run alias-gen
```
To verify its functionality, you can run the tests after installation:
```bash
poetry run pytest tests/
```

## Local Testing Setup and Execution
To test locally, first ensure all dependencies are installed:
```bash
poetry install
```

Run all tests with verbose output:
```bash
pytest -v tests/
```

Run specific test files:
```bash
pytest tests/test_aliaser.py
```

Run specific test functions:
```bash
pytest tests/test_aliaser.py::test_specific_function
```

Generate coverage report:
```bash
pytest --cov=src tests/
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
