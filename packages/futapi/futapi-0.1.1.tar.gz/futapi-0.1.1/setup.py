# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['futapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'futapi',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'S1M0N38',
    'author_email': 'bertolottosimone@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
