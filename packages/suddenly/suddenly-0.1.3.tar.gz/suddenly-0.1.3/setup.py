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
    'version': '0.1.3',
    'description': '',
    'long_description': 'suddenly\n================================================================================\n![image](https://img.shields.io/pypi/v/suddenly)\n![image](https://img.shields.io/pypi/pyversions/suddenly)\n![image](https://gitlab.com/yassu/suddenly/badges/master/pipeline.svg)\n![image](https://img.shields.io/pypi/l/suddenly)\n\n```\n$ suddenly "突然の死"                                                                                                                      0\n＿人人人人人人＿\n＞\u3000突然の死\u3000＜\n￣Y^Y^Y^Y^Y^Y^￣\n\n```\n\n# How to install\n\n```\n$ pip install suddenly\n```\n',
    'author': 'yassu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
