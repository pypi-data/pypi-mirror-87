# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airpixel']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'pyyaml>=5.3.1,<6.0.0']

extras_require = \
{'lint': ['black>=19.10b0,<20.0', 'flake8>=3.8.1,<4.0.0'],
 'monitoring': ['pyqtgraph>=0.11.0,<0.12.0', 'pyqt5>=5.15.0,<6.0.0'],
 'test': ['pytest>=5.4.2,<6.0.0'],
 'typecheck': ['mypy>=0.770,<0.771']}

setup_kwargs = {
    'name': 'airpixel',
    'version': '0.10',
    'description': 'Controll LEDs with arduinoNanoIOT and Python',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
