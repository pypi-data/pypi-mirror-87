# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_pyxl', 'nornir_pyxl.plugins', 'nornir_pyxl.plugins.tasks']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3.0.0,<4.0.0', 'openpyxl>=3.0.5,<4.0.0']

setup_kwargs = {
    'name': 'nornir-pyxl',
    'version': '0.1.4',
    'description': 'OpenPyxl plugin for nornir',
    'long_description': None,
    'author': 'Hugo',
    'author_email': 'hugotinoco@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
