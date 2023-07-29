# Developer Guide

## To update the version:
Need to manually update version in setup.py AND pyproject.toml

## Install
```bash
poetry install
```

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

https://test.pypi.org/project/alias-gen/
