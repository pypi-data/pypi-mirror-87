# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antodo']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'safer>=4.1.1,<5.0.0']

entry_points = \
{'console_scripts': ['antodo = antodo:main']}

setup_kwargs = {
    'name': 'antodo',
    'version': '0.6.0',
    'description': 'another todo app',
    'long_description': '# antodo\n\nanother todo CLI app with some useful features\n\n## Requirements\n\n- Python 3.7\n\n## Installation\n\n```shell\npip install antodo\n```\n\n## Usage\n\nadd todo\n\n```shell\nantodo add do something\n```\n\nadd urgent todo\n\n```shell\nantodo add -u do something\n```\n\nshow current todos\n\n```shell\nantodo show\n```\n\nremove todo by index based on todos order\n\n```shell\nantodo remove 1 2\n```\n\nset todo as urgent by index based on todos order\n\n```shell\nantodo urgent 3\n```\n',
    'author': 'Chabatarovich Mikita',
    'author_email': 'mikita.chabatarovich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mikitachab/antodo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
