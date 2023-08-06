# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pygit_annek']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.53,<2.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['pygit = pygit_annek.cli:main']}

setup_kwargs = {
    'name': 'pygit-annek',
    'version': '0.1.3',
    'description': 'A CLI wrapper around Pygithub',
    'long_description': '# Pygit\n\nPygit is a cli tool for managing users in Github organizations.\nIt is a wrapper for the [PyGitHub] library.\n\n\n[PyGithub]: https://github.com/PyGithub/PyGithub\n\nPyGit is a work in progress.\n\nThis project is abandoned. The new Github CLI does all this stuff.\n\n## Install\n\n\n```bash\n$ pip install pygit_annek\n```\n',
    'author': 'Michael MacKenna',
    'author_email': 'mmackenna@unitedfiregroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
