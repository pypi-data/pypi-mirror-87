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
    'version': '1.0.0',
    'description': 'Python package to work with webKnossos NML skeleton files',
    'long_description': None,
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
