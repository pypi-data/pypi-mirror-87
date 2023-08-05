# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydevice42']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'pydevice42',
    'version': '0.2.0',
    'description': 'Python library to interact with Device42',
    'long_description': '[![CI](https://github.com/post-luxembourg/pydevice42/workflows/CI/badge.svg)](https://github.com/post-luxembourg/pydevice42/actions?query=workflow%3ACI)\n[![PyPI](https://img.shields.io/pypi/v/pydevice42)](https://pypi.org/project/pydevice42/)\n\n# pydevice42\n\n## Installation\n\n```shell\npip install pydevice42\n```\n\n## Usage\n\n```python\nfrom pydevice42 import D42Client\n\nclient = D42Client(hostname="device42.com", username="admin", password="admin")\n```\n',
    'author': 'Joaquim Esteves',
    'author_email': 'joaquimbve@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/post-luxembourg/pydevice42',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
