# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectrogram_to_audio', 'spectrogram_to_audio.config']

package_data = \
{'': ['*'], 'spectrogram_to_audio.config': ['config_files/*']}

install_requires = \
['dynaconf>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'spectrogram-to-audio',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'carl2g',
    'author_email': 'degentilecarl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
