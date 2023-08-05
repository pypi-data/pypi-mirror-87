# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_estat']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.4,<2.0.0']

setup_kwargs = {
    'name': 'pandas-estat',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.7,<4.0.0',
}


setup(**setup_kwargs)
