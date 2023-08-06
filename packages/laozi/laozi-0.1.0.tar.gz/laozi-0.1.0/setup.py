# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['laozi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'laozi',
    'version': '0.1.0',
    'description': 'Serialization library outputting a human-readable format',
    'long_description': None,
    'author': 'David Francos Cuartero',
    'author_email': 'me@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
