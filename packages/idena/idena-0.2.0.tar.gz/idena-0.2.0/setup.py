# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idena', 'idena.apis']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'idena',
    'version': '0.2.0',
    'description': 'Idena RPC client',
    'long_description': ".. Idena Client documentation master file, created by\n   sphinx-quickstart on Wed Dec  2 12:50:15 2020.\n   You can adapt this file completely to your liking, but it should at least\n   contain the root `toctree` directive.\n\nIdena Client\n============\n\n.. image:: https://travis-ci.com/iRhonin/idena.py.svg?branch=main\n    :target: https://travis-ci.com/iRhonin/idena.py\n\nThis is Python wrapper for Idene Node.\n\n* Highly inspired by `Web3.py <https://github.com/ethereum/web3.py>`_ and `cookiecutter-pypackage <https://github.com/briggySmalls/cookiecutter-pypackage>`_.\n\nInstallation\n------------\n\nIdena.py can be installed using ``pip`` as follows:\n\n.. code-block:: shell\n\n   $ pip install idena\n\nFor the development, clone the repository then:\n\n.. code-block:: shell\n\n   $ poetry install\n\n\nUsing Idena\n-----------\n\nThis library depends on a connection to an Idena node and there are 2 ways to configure them. \n\nCalling `client.init` \n*********************\n\n.. code-block:: python\n\n   >>> from idena import client\n   >>> client.init('http://localhost:9009/', 'api-key')\n\n\nSetting environment variables\n*****************************\n\nSet `IDENA_RPC_NODE` and `IDENA_API_KEY` envars:\n\n.. code-block:: sh\n\n   $ export IDENA_RPC_NODE=http://localhost:9009/\n   $ export IDENA_API_KEY=api-key\n\nGetting Blockchain Info\n-----------------------\n\n.. code-block:: python\n   \n   >>> client.blockchain.get_last_block()\n      \n      Block(coinbase='0xbe854231db69ab042073b7ff8309ae3ee265a40f', \n         hash='0xa88e6ab305d7ee311ad2de35338cdbf7e664d860709e5a53f0307baeeaa6f968', \n         parentHash='0xe324a208892241e0294e5a6334965660375dda7a3ad8d8a42a5f3f2ef2857a22', \n         height=2159398, \n         timestamp=1606904853, \n         root='0xd874709bdd4c6fcd95e2e531cc07a4ce42ab23334dfd12ceb45350535b36664c', \n         identityRoot='0x9f3661f19e13d4860f2f2f1610abbbaf86abc8adf1a2781b371189e683745a97', \n         ipfsCid=None, \n         transactions=None, \n         flags=['OfflinePropose'], \n         isEmpty=False, \n         offlineAddress='0x0df427ad7e1906ab4fcc5fd31118932256f5dc7a')",
    'author': 'Arash Fatahzade',
    'author_email': 'fatahzade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iRhonin/idena.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
