# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stateman']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['APPLICATION-NAME = entry:main']}

setup_kwargs = {
    'name': 'stateman',
    'version': '1.0.4',
    'description': 'Creating binary patch files containing changes in the directory',
    'long_description': None,
    'author': 'pukhov-vi',
    'author_email': 'vipukhov@sberbank.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
