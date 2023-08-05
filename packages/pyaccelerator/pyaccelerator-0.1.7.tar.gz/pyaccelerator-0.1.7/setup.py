# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaccelerator', 'pyaccelerator.elements']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1.0,<4.0.0', 'numpy>=1.19.0,<2.0.0', 'scipy>=1.5.2,<2.0.0']

extras_require = \
{'docs': ['sphinx<3.3.0',
          'sphinx-autoapi>=1.5.0,<2.0.0',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'm2r2>=0.2.5,<0.3.0']}

setup_kwargs = {
    'name': 'pyaccelerator',
    'version': '0.1.7',
    'description': 'Accelerator building blocks.',
    'long_description': '# pyaccelerator\n\n[![Tests](https://github.com/loiccoyle/accelerator/workflows/tests/badge.svg)](https://github.com/loiccoyle/accelerator/actions?query=workflow%3Atests)\n[![Documentation Status](https://readthedocs.org/projects/pyaccelerator/badge/?version=latest)](https://pyaccelerator.readthedocs.io/en/latest/?badge=latest)\n[![pypi](https://img.shields.io/pypi/v/pyaccelerator)](https://pypi.org/project/pyaccelerator/)\n\nPython package to build simple toy accelerators.\n\n# Dependencies:\n  * `numpy`\n  * `matplotlib`\n  * `scipy`\n\n# Installation:\n\n```sh\npip install pyaccelerator\n```\n\nIt usualy a good idea to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html). To create a virtual environment in the `venv` folder (assuming python3):\n```sh\npython -m venv venv\n```\n\nTo activate the virtual environment:\n```sh\nsource venv/bin/activate\n```\n\nProceed with the installation to install in the virtual environment.\n\nTo deactivate the virtual environment:\n```sh\ndeactivate\n```\n\n# Usage:\nSee the `notebooks` folder for some examples.\n',
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle <loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loiccoyle/pyaccelerator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
