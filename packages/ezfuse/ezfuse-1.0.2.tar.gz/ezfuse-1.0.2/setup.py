# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezfuse']

package_data = \
{'': ['*']}

install_requires = \
['colorama']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata']}

entry_points = \
{'console_scripts': ['ezfuse = ezfuse.cli:run']}

setup_kwargs = {
    'name': 'ezfuse',
    'version': '1.0.2',
    'description': 'Quickly mount fuse filesystems in temporary directories',
    'long_description': None,
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
