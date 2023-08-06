# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helloworld_stunning_tribble']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['helloworld-stunning-tribble = '
                     'helloworld_stunning_tribble.main:cli']}

setup_kwargs = {
    'name': 'helloworld-stunning-tribble',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Wesley Batista',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
