# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mhealthlab_client', 'mhealthlab_client.tests']

package_data = \
{'': ['*']}

install_requires = \
['arus-muss>=0.2.0,<0.3.0',
 'arus>=1.1.18,<2.0.0',
 'outdated>=0.2.0,<0.3.0',
 'pysftp>=0.2.9,<0.3.0',
 'pyzipper>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['mhlab = mhealthlab_client.mhlab:mhlab']}

setup_kwargs = {
    'name': 'mhealthlab-client',
    'version': '0.8.2',
    'description': 'Client to download and decrypt data for lab projects of mhealthgroup.org',
    'long_description': None,
    'author': 'Qu Tang',
    'author_email': 'tang.q@northeastern.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
