# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duniterpy',
 'duniterpy.api',
 'duniterpy.api.bma',
 'duniterpy.api.elasticsearch',
 'duniterpy.api.ws2p',
 'duniterpy.documents',
 'duniterpy.documents.ws2p',
 'duniterpy.grammars',
 'duniterpy.helpers',
 'duniterpy.key']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.3,<4.0.0',
 'attrs>=20.2.0,<21.0.0',
 'base58>=2.0.0,<3.0.0',
 'graphql-core>=3.1.2,<4.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'libnacl>=1.7.2,<2.0.0',
 'pyaes>=1.6.1,<2.0.0',
 'pypeg2>=2.15.2,<3.0.0']

setup_kwargs = {
    'name': 'duniterpy',
    'version': '0.61.0',
    'description': 'Python library for developers of Duniter clients',
    'long_description': "# Duniter Python API\n\nPython implementation for [Duniter](https://git.duniter.org/nodes/typescript/duniter) BMA API\n\nThis is the most complete Python library to communicate with Duniter nodes endpoints.\n\nThis library is used by two clients:\n- [Sakia](http://sakia-wallet.org/), the rich client to manage your Duniter's wallets.\n- [Silkaj](https://silkaj.duniter.org/), the command line client.\n\n## Features\n- Support Duniter's [Basic Merkle API](https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md) and [protocol](https://git.duniter.org/nodes/common/doc/blob/master/rfc/0009_Duniter_Blockchain_Protocol_V11.md)\n- Asynchronous/synchronous without threads\n- Support HTTP, HTTPS and Web Socket transport for the BMA API\n- Support [Elasticsearch Duniter4j](https://git.duniter.org/clients/java/duniter4j/blob/master/src/site/markdown/ES.md#request-the-es-node>) API\n- Duniter signing key\n- Sign/verify and encrypt/decrypt messages with the Duniter credentials\n\n## Requirements\n- Python >= 3.6.8\n- [aiohttp >= 3.6.3](https://pypi.org/project/aiohttp)\n- [jsonschema](https://pypi.org/project/jsonschema)\n- [pyPEG2](https://pypi.org/project/pyPEG2)\n- [attrs](https://pypi.org/project/attrs)\n- [base58](https://pypi.org/project/base58)\n- [libnacl](https://pypi.org/project/libnacl)\n- [pyaes](https://pypi.org/project/pyaes)\n\n## Installation\nYou can install DuniterPy and its dependencies with the following command:\n```bash\npip3 install duniterpy --user\n```\n\n## Install the development environment\n- Install [Poetry](https://poetry.eustace.io):\n```bash\ncurl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python - --preview\n```\n\n## Documentation\nOnline official automaticaly generated documentation: https://clients.duniter.io/python/duniterpy/index.html\n\nThe [examples folder](https://git.duniter.org/clients/python/duniterpy/tree/master/examples) contains scripts to help you!\n\nPlease take a look at the document [HTTP API](https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md) to learn more about the BMA API.\n\nHow to generate and read locally the autodoc:\n\n- Install Sphinx\n```bash\npoetry install -E sphinx\n```\n\n- Generate documentation\n```bash\npoetry run make docs\n```\n\n- The HTML documentation is generated in `docs/_build/html` folder.\n\n## Development\n* When writing docstrings, use the reStructuredText format recommended by https://www.python.org/dev/peps/pep-0287/#docstring-significant-features\n* Use make commands to check the code and the format.\n\nBlack, the formatting tool, requires Python 3.6 or higher.\n\n* Install runtime dependencies\n```bash\npoetry install --no-dev\n```\n\n* Have a look at the examples folder\n* Run examples from parent folder\n```bash\npoetry run python examples/request_data.py\n```\n\n* Before submitting a merge requests, please check the static typing and tests.\n\n* Install dev dependencies\n```bash\npoetry install\n```\n\n* Check static typing with [mypy](http://mypy-lang.org/)\n```bash\nmake check\n```\n\n* Run all unit tests (builtin `unittest` module) with:\n```bash\nmake tests\n```\n\n* Run only some unit tests by passing a special ENV variable:\n```bash\nmake tests TESTS_FILTER=tests.documents.test_block.TestBlock.test_fromraw\n```\n\n## Packaging and deploy\n### PyPi\nChange and commit and tag the new version number (semantic version number)\n```bash\n./release.sh 0.42.3\n```\n\nBuild the PyPi package in the `dist` folder\n```bash\nmake build\n```\n\nDeploy the package to PyPi test repository (prefix the command with a space in order for the shell not to save in its history system the command containing the password)\n```bash\n[SPACE]make deploy_test PYPI_TEST_LOGIN=xxxx PYPI_TEST_PASSWORD=xxxx\n```\n\nInstall the package from PyPi test repository\n```bash\npip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple/ duniterpy\n```\n\nDeploy the package on the PyPi repository (prefix the command with a space in order for the shell not to save in its history system the command containing the password)\n```bash\n[SPACE]make deploy PYPI_LOGIN=xxxx PYPI_PASSWORD=xxxx\n```\n\n## Packaging status\n[![Packaging status](https://repology.org/badge/vertical-allrepos/python:duniterpy.svg)](https://repology.org/project/python:duniterpy/versions)\n",
    'author': 'inso',
    'author_email': 'insomniak.fr@gmail.com',
    'maintainer': 'vit',
    'maintainer_email': 'vit@free.fr',
    'url': 'https://git.duniter.org/clients/python/duniterpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
