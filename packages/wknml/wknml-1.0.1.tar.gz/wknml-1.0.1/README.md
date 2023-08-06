# wknml
[![PyPI version](https://img.shields.io/pypi/v/wknml)](https://pypi.python.org/pypi/wknml)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/wknml.svg)](https://pypi.python.org/pypi/wknml)
[![Build Status](https://img.shields.io/github/workflow/status/scalableminds/wknml/Test%20Python%20Package/master)](https://github.com/scalableminds/wknml/actions?query=workflow%3A%22Test+Python+Package%22)
[![Documentation](https://img.shields.io/badge/docs-passing-brightgreen.svg)](https://github.com/scalableminds/wknml/blob/master/docs/wknml.md)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python library for working with [webKnossos](https://webknossos.org) [skeleton annotation files (NML)](https://docs.webknossos.org/reference/data_formats#nml).

## Installation
wknml requires Python 3.6+

```
pip install wknml
```

## Documentation

See [docs/wknml.md](docs/wknml.md) for an API documentation.

## Examples

Some examples to get you started. Make sure to also check the `examples` directory:

```python
# Load an NML file
with open("input.nml", "rb") as f:
    nml = wknml.parse_nml(f, nml)

# Access the most important properties
print(nml.parameters)
print(nml.trees)
print(nml.branchpoints)
print(nml.comments)
print(nml.groups)

# Iterate over all nodes
for tree in nml.trees:
    for node in tree.nodes:
        print(tree, node)

# Write a new NML file to disk
with open("out.nml", "wb") as f:
    wknml.write_nml(f, nml)
```

```bash
# Convert an NML file with unlinked nodes to one with connected trees
python -m examples.fix_unlinked_nml <unlinked>.nml <fixed>.nml
```

# Development
Make sure to install all the required dependencies using Poetry:
```
pip install poetry
poetry install
```

Please, format and test your code changes before merging them.
```
poetry run black wknml tests examples
poetry run pytest tests
```

PyPi releases are automatically pushed when creating a new Git tag/Github release. Make sure to bump the package version number manually:
```
poetry version <patch, minor, major>
```

If necessary, rebuild the documentation and commit to repository:
```
poetry run pydoc-markdown -m wknml --render-toc > docs/wknml.md
```

# License

MIT License
