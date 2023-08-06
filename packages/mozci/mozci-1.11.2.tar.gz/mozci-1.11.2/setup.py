# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozci',
 'mozci.data',
 'mozci.data.sources',
 'mozci.data.sources.activedata',
 'mozci.data.sources.hgmo',
 'mozci.data.sources.taskcluster',
 'mozci.data.sources.treeherder',
 'mozci.util']

package_data = \
{'': ['*'], 'mozci.data.sources.activedata': ['queries/*']}

install_requires = \
['adr>=0.19,<0.20',
 'aiohttp>=3.6.3,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'cachy>=0.3.0,<0.4.0',
 'flake8>=3.8.3,<4.0.0',
 'loguru>=0.5.1,<0.6.0',
 'requests>=2.24.0,<3.0.0',
 'taskcluster>=30.1.1,<31.0.0',
 'taskcluster_urls>=12.1,<14.0',
 'tomlkit>=0.6.0,<0.7.0',
 'voluptuous>=0.11.7,<0.13.0']

setup_kwargs = {
    'name': 'mozci',
    'version': '1.11.2',
    'description': '',
    'long_description': None,
    'author': 'Andrew Halberstadt',
    'author_email': 'ahal@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
