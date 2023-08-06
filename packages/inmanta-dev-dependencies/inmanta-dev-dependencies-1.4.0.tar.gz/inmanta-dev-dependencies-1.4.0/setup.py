# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inmanta_dev_dependencies']

package_data = \
{'': ['*']}

install_requires = \
['black==20.8b1',
 'flake8-black==0.2.1',
 'flake8-copyright==0.2.2',
 'flake8-isort==4.0.0',
 'flake8==3.8.4',
 'isort==5.6.4',
 'lxml==4.6.2',
 'mypy==0.790',
 'pytest==6.1.2']

extras_require = \
{'async': ['pytest-asyncio==0.14.0', 'pytest-timeout==1.4.2'],
 'extension': ['tox==3.20.1', 'tox-venv==0.4.0'],
 'module': ['pytest-inmanta==1.4.0']}

setup_kwargs = {
    'name': 'inmanta-dev-dependencies',
    'version': '1.4.0',
    'description': 'Package collecting all common dev dependencies of inmanta modules and extensions to synchronize dependency versions.',
    'long_description': None,
    'author': 'Inmanta',
    'author_email': 'code@inmanta.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
