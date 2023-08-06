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
    'version': '1.1.0',
    'description': 'An ID manager for git',
    'long_description': '# git-id\nAn ID manager for git\n\n# how to install\n\n```\n$ pip install git-id\n```\n',
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
