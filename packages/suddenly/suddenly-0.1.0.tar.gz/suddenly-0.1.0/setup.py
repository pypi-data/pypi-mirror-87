# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suddenly']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['suddenly = suddenly.suddenly:main']}

setup_kwargs = {
    'name': 'suddenly',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yassu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
