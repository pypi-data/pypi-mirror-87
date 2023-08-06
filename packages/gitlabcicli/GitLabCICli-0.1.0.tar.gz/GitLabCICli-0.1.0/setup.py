# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlabcicli',
 'gitlabcicli.api',
 'gitlabcicli.api.models',
 'gitlabcicli.managerlib']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.11,<4.0.0',
 'argcomplete>=1.12.2,<2.0.0',
 'dbus-python>=1.2.16,<2.0.0',
 'keyring>=21.5.0,<22.0.0',
 'requests>=2.25.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['gitlabcicli = gitlabcicli.gitlabcicli:main']}

setup_kwargs = {
    'name': 'gitlabcicli',
    'version': '0.1.0',
    'description': 'Command line interface for GitLab CI',
    'long_description': None,
    'author': 'sedrubal',
    'author_email': 'dev@sedrubal.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/sedrubal/gitlabcicli.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
