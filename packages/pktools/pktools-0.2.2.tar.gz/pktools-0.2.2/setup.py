# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pktools']

package_data = \
{'': ['*']}

install_requires = \
['ccxt>=1.38.50,<2.0.0', 'requests>=2.25.0,<3.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'pktools',
    'version': '0.2.2',
    'description': '',
    'long_description': '# pktools\n\nPython uilities',
    'author': 'katmai',
    'author_email': 'katmai.mobil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
