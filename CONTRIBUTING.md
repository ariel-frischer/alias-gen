## TODO

- [ ] Have python alias-gen module run cli commands easier, rather then having
      to run the .py script from ./src/alias_gen/aliaser.py. It should be
      simpler, something like: `python -m alias-gen mycommand`
- [ ] Fix comands that start with ./script.sh cannot have alias of . or / or
      ~ or \_.
- [ ] Put more debug statements in stategic places
- [ ] Add arg to allow alias for fish over abbr.

- [ ] Add gitlab pipelines for quality of code / linting.
- [ ] Add pipeline for vulnerabilities/secrets.
- [ ] Package everything with poetry.
- [ ] Publish to public gitlab
- [ ] Publish to public github
- [ ] Write an article about this and how ChatGPT helped write boilerplate.
- [ ] Publish my own website with that article.
- [x] Test out publish + version bumping using twine + setuptools
- [x] Move this script into its own repo
- [x] Add an MIT license

## Dev Notes

https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-7be9dd5d6dcd

# To update our build version:

## Update version in setup.py AND pyproject.toml

```bash
python setup.py sdist bdist_wheel
```

## Upload to pypi

```bash
python -m twine upload --repository testpypi dist/\* --skip-existing
```

