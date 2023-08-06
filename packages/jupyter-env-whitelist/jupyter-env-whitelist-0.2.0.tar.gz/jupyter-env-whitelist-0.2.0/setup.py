# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_env_whitelist']

package_data = \
{'': ['*']}

install_requires = \
['notebook>=6.0,<7.0']

setup_kwargs = {
    'name': 'jupyter-env-whitelist',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Daisuke Taniwaki',
    'author_email': 'daisuketaniwaki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
