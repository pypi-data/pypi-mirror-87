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
    'version': '1.2.1',
    'description': 'Creating binary patch files containing changes in the directory',
    'long_description': 'Creating binary patch files containing changes in the directory\n\n## Simple usage :\n```\nfrom stateman import GetState, GetDiff, CreatePatch, ApplyPatch\nimport os\nimport shutil\npatch_file="new.patch"\n\ndef write_file(filename, text):\n    with open(filename,\'w\') as f:\n        f.write(text)\n\n\n# Clear workspace\nif os.path.exists(".tmp"):\n    shutil.rmtree(".tmp")\nif os.path.exists(".tmp2"):\n    shutil.rmtree(".tmp2")\n\n\n# Init workspace .tmp with one subfolder\nroot_dir = os.path.abspath(".tmp")\ntarget_dir = os.path.abspath(".tmp2")\nos.makedirs(".tmp")\nsubfolder = os.path.join(root_dir,".git")\nos.makedirs(subfolder)\n\n# Create files in workspace\nwrite_file(os.path.join(subfolder,"testfile1.txt"), "test1")\nwrite_file(os.path.join(subfolder,"testfile2.txt"), "test2")\nwrite_file(os.path.join(root_dir,"testfile3.txt"), "test3")\nwrite_file(os.path.join(root_dir,"testfile4.txt"), "test4")\n\n# Get state of workspace\nstate1 = GetState(root_dir, exclude = r\'.git\'+os.path.sep)\nprint(state1)\n\n# Make a copy of workspace\nshutil.copytree(root_dir, target_dir)\n\n# Make a changes\nos.remove(os.path.join(subfolder,"testfile2.txt"))\nos.remove(os.path.join(root_dir,"testfile4.txt"))\nwrite_file(os.path.join(subfolder,"testfile2.txt"), "changed")\n\n# Get state of workspace after changes\nstate2 = GetState(root_dir, exclude = r\'.git\'+os.path.sep)\nprint(state2)\n\n# Get diff between spaces\ndiff = GetDiff(state1, state2)\nprint (diff)\n\n# Create patch file\nCreatePatch(root_dir, patch_file, diff)  \n\n# Apply patch on copy of workspace, maked before changes\nApplyPatch(target_dir, patch_file, exclude = r\'.git\'+os.path.sep)\n\n# Copy of workspace after apply patch identical as workspace \n```\n\n## Source Code:\n* [https://github.com/vpuhoff/stateman](https://github.com/vpuhoff/stateman)\n\n## Travis CI Deploys:\n* [https://travis-ci.com/vpuhoff/patchgen](https://travis-ci.com/vpuhoff/patchgen) [![Build Status](https://travis-ci.com/vpuhoff/patchgen.svg?branch=master)](https://travis-ci.com/vpuhoff/patchgen)',
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
