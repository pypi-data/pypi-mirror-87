# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catmeow']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'setuptools>=50.3.2,<51.0.0']

entry_points = \
{'console_scripts': ['catmeow = catmeow:main']}

setup_kwargs = {
    'name': 'catmeow',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Sergey Royz',
    'author_email': 'zjor.se@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
