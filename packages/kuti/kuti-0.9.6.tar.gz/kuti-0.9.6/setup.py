# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuti', 'kuti..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7,<8',
 'future',
 'h5py>=2.10.0,<3.0.0',
 'matplotlib',
 'munch',
 'numpy',
 'opencv-python',
 'pandas',
 'scikit-image>=0.16.2,<0.17.0',
 'scikit-learn>=0.22.1,<0.23.0',
 'scipy']

setup_kwargs = {
    'name': 'kuti',
    'version': '0.9.6',
    'description': 'Keras training management utilities.',
    'long_description': '# Keras utilities (Kuti)\n\nThe project contains utilities for image assessment development with Keras/Tensorflow, including utilities for model training, custom generators, image management and augmentation. This is a poetry package for [ku](https://github.com/subpic/ku).\n\nThe library requires tensorflow >= 1.14 or 2.x installed.\n\n    $ pip install kuti\n\n## Overview\n\nSome of the key components of each file:\n\n**`model_helper.py`**:\n\n* `ModelHelper`: Wrapper class that simplifies default usage of Keras for regression models.\n\n**`generators.py`**:\n\n* `DataGeneratorDisk`, `DataGeneratorHDF5`: Keras generators for on-disk images, and HDF5 stored features/images\n\n**`image_utils.py`**:\n\n* various utility functions for manipulating images (read, write to HDF5, batch resize, view batch)\n\n**`image_augmenter.py`**:\n\n* `ImageAugmenter`: Create custom image augmentation functions for training Keras models.\n\n**`generic.py`**:\n\n* `H5Helper`: Manage named data sets in HDF5 files, for us in Keras generators.\n* `ShortNameBuilder`: Utility for building short (file) names that contain multiple parameters.\n\n**`applications.py`**:\n\n* `model_inception_multigap`, `model_inceptionresnet_multigap`: Model definitions for extracting MLSP narrow features\n* `model_inception_pooled`, `model_inceptionresnet_pooled`: Model definitions for extracting MLSP wide features\n\nYou can find more information in the docstrings.\n',
    'author': 'Vlad Hosu',
    'author_email': 'subpic@gmail.com',
    'maintainer': 'Vlad Hosu',
    'maintainer_email': 'subpic@gmail.com',
    'url': 'https://github.com/subpic/ku/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
