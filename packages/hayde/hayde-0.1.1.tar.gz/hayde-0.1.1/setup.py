# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hayde']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0',
 'Jinja2>=2.11.2,<3.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'kubernetes>=12.0.1,<13.0.0']

entry_points = \
{'console_scripts': ['hayde = hayde.cli:main']}

setup_kwargs = {
    'name': 'hayde',
    'version': '0.1.1',
    'description': 'Hayde',
    'long_description': "# hayde [![PyPi version](https://img.shields.io/pypi/v/hayde.svg)](https://pypi.python.org/pypi/hayde/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/hayde.svg)](https://pypi.python.org/pypi/hayde/) [![](https://img.shields.io/gitlab/license/f9n/hayde.svg)](https://gitlab.com/f9n/hayde/blob/master/LICENSE)\n\nHayde\n\n# Installation\n\n```bash\n$ python3 -m pip install --user --upgrade hayde\n```\n\n# Usage\n\n```bash\n$ hayde -h\nusage: Hayde [-h] --config-file CONFIG_FILE [--version]\n\nHayde\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --config-file CONFIG_FILE\n  --version             show program's version number and exit\n```\n",
    'author': 'f9n',
    'author_email': 'f9n@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/f9n/hayde',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
