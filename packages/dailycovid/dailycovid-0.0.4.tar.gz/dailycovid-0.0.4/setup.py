# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dailycovid']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.0.0,<2.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dailycovid = dailycovid:main']}

setup_kwargs = {
    'name': 'dailycovid',
    'version': '0.0.4',
    'description': 'U.S.A daily covid information',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
