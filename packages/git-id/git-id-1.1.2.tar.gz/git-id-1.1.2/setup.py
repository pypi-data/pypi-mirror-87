# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_id']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'gitpython>=3.1.9,<4.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['git-id = git_id.core:main']}

setup_kwargs = {
    'name': 'git-id',
    'version': '1.1.2',
    'description': 'An ID manager for git',
    'long_description': '# git-id\n[![PyPI version](https://badge.fury.io/py/git-id.svg)](https://badge.fury.io/py/git-id)\n\n\nAn ID manager for git.\n\nAn Identity / Profile consists of name, email, and signingkey, and this command aims to manage them and help switch between them seamlessly.\n\n# how to install\n\n```\n$ pip install git-id\n```\n\n# Usage\n\n## `info` - show info / add identity\n```\n$ git id info\n```\n\n`info` will retrieve identity from current repository and search a matching identity in the registry (`$HOME/.git-id.yml`).\n\nIf no matching identity is found, then asks you if you want to register it.\n\n## `ls` - list identities in the registry\n```\n$ git id ls\n```\n\n`ls` will show all the identities in the registry.\n\n## `use` - use an identity\n```\n$ git id use <profile_id>\n```\n\n`use` will set the identity of the current repository to the identity `<profile_id>` in the registry.\n\n## `create` - create an identity\n```\n$ git id create\n```\n\n`create` will create + register a new identity interactively/non-interactively.\n',
    'author': 'Yuichiro Smith',
    'author_email': 'contact@yu-smith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yu-ichiro/git-id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
