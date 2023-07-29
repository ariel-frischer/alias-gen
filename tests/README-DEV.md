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

## References

https://pypi.org/project/alias-gen/
https://test.pypi.org/project/alias-gen/
