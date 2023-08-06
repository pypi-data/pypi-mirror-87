# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wknml']

package_data = \
{'': ['*']}

install_requires = \
['loxun==2.0', 'networkx>=2.5,<3.0', 'numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'wknml',
    'version': '1.0.1',
    'description': 'Python package to work with webKnossos NML skeleton files',
    'long_description': '# wknml\n[![PyPI version](https://img.shields.io/pypi/v/wknml)](https://pypi.python.org/pypi/wknml)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/wknml.svg)](https://pypi.python.org/pypi/wknml)\n[![Build Status](https://img.shields.io/github/workflow/status/scalableminds/wknml/Test%20Python%20Package/master)](https://github.com/scalableminds/wknml/actions?query=workflow%3A%22Test+Python+Package%22)\n[![Documentation](https://img.shields.io/badge/docs-passing-brightgreen.svg)](https://github.com/scalableminds/wknml/blob/master/docs/wknml.md)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython library for working with [webKnossos](https://webknossos.org) [skeleton annotation files (NML)](https://docs.webknossos.org/reference/data_formats#nml).\n\n## Installation\nwknml requires Python 3.6+\n\n```\npip install wknml\n```\n\n## Documentation\n\nSee [docs/wknml.md](docs/wknml.md) for an API documentation.\n\n## Examples\n\nSome examples to get you started. Make sure to also check the `examples` directory:\n\n```python\n# Load an NML file\nwith open("input.nml", "rb") as f:\n    nml = wknml.parse_nml(f, nml)\n\n# Access the most important properties\nprint(nml.parameters)\nprint(nml.trees)\nprint(nml.branchpoints)\nprint(nml.comments)\nprint(nml.groups)\n\n# Iterate over all nodes\nfor tree in nml.trees:\n    for node in tree.nodes:\n        print(tree, node)\n\n# Write a new NML file to disk\nwith open("out.nml", "wb") as f:\n    wknml.write_nml(f, nml)\n```\n\n```bash\n# Convert an NML file with unlinked nodes to one with connected trees\npython -m examples.fix_unlinked_nml <unlinked>.nml <fixed>.nml\n```\n\n# Development\nMake sure to install all the required dependencies using Poetry:\n```\npip install poetry\npoetry install\n```\n\nPlease, format and test your code changes before merging them.\n```\npoetry run black wknml tests examples\npoetry run pytest tests\n```\n\nPyPi releases are automatically pushed when creating a new Git tag/Github release. Make sure to bump the package version number manually:\n```\npoetry version <patch, minor, major>\n```\n\nIf necessary, rebuild the documentation and commit to repository:\n```\npoetry run pydoc-markdown -m wknml --render-toc > docs/wknml.md\n```\n\n# License\n\nMIT License\n',
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scalableminds/wknml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
