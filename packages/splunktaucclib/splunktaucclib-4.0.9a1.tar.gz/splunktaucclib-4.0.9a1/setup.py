# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunktaucclib',
 'splunktaucclib.common',
 'splunktaucclib.data_collection',
 'splunktaucclib.global_config',
 'splunktaucclib.rest_handler',
 'splunktaucclib.rest_handler.endpoint',
 'splunktaucclib.splunk_aoblib']

package_data = \
{'': ['*']}

install_requires = \
['future>=0,<1',
 'solnlib>=3,<4',
 'splunk-sdk>=1.6,<2.0',
 'splunktalib>=1.1,<2.0']

setup_kwargs = {
    'name': 'splunktaucclib',
    'version': '4.0.9a1',
    'description': '',
    'long_description': None,
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
