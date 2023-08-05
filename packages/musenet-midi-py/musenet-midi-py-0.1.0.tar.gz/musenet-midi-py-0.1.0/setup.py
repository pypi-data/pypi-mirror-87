# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musenet_midi_py']

package_data = \
{'': ['*']}

install_requires = \
['mido>=1.2.9,<2.0.0']

setup_kwargs = {
    'name': 'musenet-midi-py',
    'version': '0.1.0',
    'description': 'MuseNet Midi encoder and decoder',
    'long_description': None,
    'author': 'daanklijn',
    'author_email': 'daanklijn0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
