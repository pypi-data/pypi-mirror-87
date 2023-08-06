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
    'version': '1.0.7',
    'description': 'Creating binary patch files containing changes in the directory',
    'long_description': 'Creating binary patch files containing changes in the directory\n\n## Simple usage :\n```\nroot_dir = os.path.abspath(".tmp")\npatch_file="new.patch"\n# Get snapshot metadata of folder\nstate1 = GetState(root_dir)\n\n# change files\n\n# Get snapshot metadata of folder after changes\nstate2 = GetState(root_dir)\n\n# Calculate diff\ndiff = GetDiff(state1, state2)\n\n# Create patch file\nCreatePatch(root_dir, patch_file, diff)  \n\n# Apply patch file\nApplyPatch(root_dir, patch_file)\n```\n\n## Source Code:\n* [https://github.com/vpuhoff/stateman](https://github.com/vpuhoff/stateman)\n\n## Travis CI Deploys:\n* [https://travis-ci.com/vpuhoff/patchgen](https://travis-ci.com/vpuhoff/stateman) [![Build Status](https://travis-ci.com/vpuhoff/patchgen.svg?branch=master)](https://travis-ci.com/vpuhoff/stateman)',
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
