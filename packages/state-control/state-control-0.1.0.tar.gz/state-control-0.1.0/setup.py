# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['state_control']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'state-control',
    'version': '0.1.0',
    'description': 'A simple state machine library',
    'long_description': '# State Control\n',
    'author': 'AlwinW',
    'author_email': '16846521+AlwinW@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
