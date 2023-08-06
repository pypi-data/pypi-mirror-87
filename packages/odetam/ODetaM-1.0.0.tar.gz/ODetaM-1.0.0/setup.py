# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odetam']

package_data = \
{'': ['*']}

install_requires = \
['deta>=0.7.0,<0.8.0', 'pydantic>=1.7,<2.0', 'ujson>=4.0,<5.0']

setup_kwargs = {
    'name': 'odetam',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Rick Henry',
    'author_email': 'rickhenry@rickhenry.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
