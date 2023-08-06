# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beneath',
 'beneath.admin',
 'beneath.beam',
 'beneath.bin',
 'beneath.cli',
 'beneath.pipeline',
 'beneath.proto',
 'beneath.utils']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.15,<0.30.0',
 'aiogrpc>=1.7,<2.0',
 'aiohttp>=3.6.2,<4.0.0',
 'argparse>=1.4,<2.0',
 'fastavro>=0.22,<0.23',
 'grpcio==1.27.2',
 'msgpack>=1.0.0,<2.0.0',
 'pandas>=1.0.1,<2.0.0',
 'protobuf>=3.11.3,<4.0.0',
 'six>=1.14.0,<2.0.0']

entry_points = \
{'console_scripts': ['beneath = beneath.cli:main']}

setup_kwargs = {
    'name': 'beneath',
    'version': '1.2.9',
    'description': 'Python client and CLI for Beneath (https://beneath.dev/)',
    'long_description': "# Beneath Python Client Library\n\n[![PyPI version](https://img.shields.io/pypi/v/beneath.svg)](https://pypi.org/project/beneath)\n[![Docs badge](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://python.docs.beneath.dev)\n[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)\n[![Netlify Status](https://api.netlify.com/api/v1/badges/e2dacc5a-486e-4043-9a42-350acb658efc/deploy-status)](https://app.netlify.com/sites/beneath-clients-python/deploys)\n\nThis folder contains the source code for the [Beneath](https://beneath.dev) Python library. Here are some useful links:\n\n- [Beneath Docs](https://about.beneath.dev/docs/)\n- [Python Client API Reference](https://python.docs.beneath.dev)\n- [Reading data tutorial](https://about.beneath.dev/docs/read-data-into-jupyter-notebook/)\n- [Writing data tutorial](https://about.beneath.dev/docs/write-data-from-your-app/)\n\n### Providing feedback\n\nBeneath is just entering public beta, so there's bound to be some rough edges. Bugs, feature requests, suggestions – we'd love to hear about them. To file an issue, [click here](https://gitlab.com/beneath-hq/beneath/issues).\n",
    'author': 'Beneath Systems',
    'author_email': 'hello@beneath.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/beneath-hq/beneath/-/tree/master/clients/python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
