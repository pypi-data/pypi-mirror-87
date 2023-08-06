# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jubeatnet']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'jubeatnet',
    'version': '0.2.0',
    'description': 'End to End solution for analyzing, modelling and visualizing Jubeat songs and player fingering techniques.',
    'long_description': None,
    'author': 'Chester',
    'author_email': 'chester8991@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
