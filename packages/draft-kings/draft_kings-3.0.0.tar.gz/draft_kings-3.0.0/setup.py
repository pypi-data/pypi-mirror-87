# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['draft_kings',
 'draft_kings.output',
 'draft_kings.output.objects',
 'draft_kings.output.schema',
 'draft_kings.output.transformers',
 'draft_kings.response',
 'draft_kings.response.objects',
 'draft_kings.response.schema']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow-enum>=1.5.1,<2.0.0',
 'marshmallow>=3.9.1,<4.0.0',
 'requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'draft-kings',
    'version': '3.0.0',
    'description': 'A client to access data on draftkings.com',
    'long_description': '![GitHub Actions](https://github.com/jaebradley/draftkings_client/workflows/DraftKings%20Client/badge.svg?branch=v3)\n![codecov](https://codecov.io/gh/jaebradley/draftkings_client/branch/v3/graph/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/draft_kings.svg)\n\n# DraftKings Python Client\n\n## Introduction\n\nTo the best of my knowledge, **DraftKings** does not have an "official", well-documented public-facing API.\n\nInstead, they have various **HTTP** endpoints that do not require authentication (so are "public" in this manner).\n\nThese "public" endpoints allow one to fetch data for various resources including contests for a specific sport, or\nplayers that are draftable for a given contest (as well as relevant metadata).\n\nAs **DraftKings** makes no guarantees about it\'s "public" API, this client makes no guarantees that the existing API \nmethods will work consistently.\n\n## Documentation\n\nFor documentation about package installation as well as the client\'s API, please see \n[the documentation site](https://jaebradley.github.io/draftkings_client).\n',
    'author': 'Jae Bradley',
    'author_email': 'jae.b.bradley@gmail.com',
    'maintainer': 'Jae Bradley',
    'maintainer_email': 'jae.b.bradley@gmail.com',
    'url': 'https://jaebradley.github.io/draftkings_client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
