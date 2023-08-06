# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dailycovid']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0.0,<4.0.0', 'numpy>=1.0.0,<2.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dailycovid = dailycovid:main']}

setup_kwargs = {
    'name': 'dailycovid',
    'version': '0.1.2',
    'description': 'U.S.A daily covid information',
    'long_description': '# dailycovid - Easily get covid updates\n\n# Pypi installation\n`pip3 install dailycovid`\n\n# Usage\n\nTo get the plots for every county in a state.\n\n`dailycovid -state ny`\n\nOr by county.\n\n`daily covid -state CA -county "Los Angeles"`\n\n# Examples of plots\n\n![image](examples/plots_los_angeles_california.png)\n\n![image](examples/plots_suffolk_massachusetts.png)\n\n![image](examples/plots_new_york_city_new_york.png)\n',
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
