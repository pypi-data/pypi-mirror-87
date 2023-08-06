# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lantern', 'lantern.functional', 'lantern.numpy']

package_data = \
{'': ['*']}

install_requires = \
['imgaug>=0.4.0,<0.5.0',
 'numpy>=1.19.4,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pytorch-datastream>=0.3.8,<0.4.0',
 'tensorboard>=2.2.0,<3.0.0',
 'torch>=1.6.0,<2.0.0',
 'tqdm>=4.51.0,<5.0.0']

setup_kwargs = {
    'name': 'pytorch-lantern',
    'version': '0.9.1',
    'description': 'Pytorch project template and related tools',
    'long_description': None,
    'author': 'Aiwizo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
