# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotgallery']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.2.3,<3.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'plotgallery',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'shughes',
    'author_email': 'shughes.uk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
