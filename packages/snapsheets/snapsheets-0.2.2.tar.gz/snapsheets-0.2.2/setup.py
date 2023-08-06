# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapsheets']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'snapsheets',
    'version': '0.2.2',
    'description': 'Wget snapshots of google sheets',
    'long_description': "![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)\n![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)\n\n\n# Snapsheets\n\nWget snapshots of Google \n\n---\n\n# Usage\n\n```python\n>>> import snapsheets as ss\n>>> ss.add_config('test_config.yml')\n>>> ss.get('test1', by='wget')\n```\n\n---\n\n## Config\n\n- Write config file in ``YAML`` format\n\n```yaml\nvolumes:\n  snapd: 'data/'\n\noptions:\n  wget:\n    '--quiet'\n    \nsheets:\n  test1:\n    key: '1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM'\n    gid: 'None'\n    format: 'xlsx'\n    sheet_name:\n      - 'シート1'\n      - 'シート2'\n    stem: 'test_sheet'\n    datefmt: '%Y'\n```\n\n---\n\n# Documents\n\n- https://shotakaha.gitlab.io/snapsheets/\n",
    'author': 'shotakaha',
    'author_email': 'shotakaha+py@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://shotakaha.gitlab.io/snapsheets/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
