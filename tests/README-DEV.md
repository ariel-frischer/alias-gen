# Developer Guide

## To update the version:
Need to manually update version in setup.py AND pyproject.toml

## Create a new build
```bash
python setup.py sdist bdist_wheel
```

## Check the distribution is valid
```bash
twine check dist/*python -m twine upload dist/* --skip-existingpython setup.py sdist bdist_wheel
```

## Create a new build
```bash
python -m twine upload dist/* --skip-existingpython setup.py sdist bdist_wheel
```


