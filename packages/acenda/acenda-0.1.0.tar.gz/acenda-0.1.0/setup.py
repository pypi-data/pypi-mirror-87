# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acenda']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'acenda',
    'version': '0.1.0',
    'description': 'acenda python sdk',
    'long_description': None,
    'author': 'nicksherron',
    'author_email': 'nsherron90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicksherron/acenda-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
