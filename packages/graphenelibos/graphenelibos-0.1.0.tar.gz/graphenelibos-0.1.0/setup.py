# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphenelibos']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['graphene-sgx-get-token = '
                     'graphenelibos.sgx_get_token:main',
                     'graphene-sgx-sign = graphenelibos.sgx_sign:main']}

setup_kwargs = {
    'name': 'graphenelibos',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'graphene-project.io',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
