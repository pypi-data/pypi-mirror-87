# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastnn',
 'fastnn.nn',
 'fastnn.processors',
 'fastnn.processors.cv',
 'fastnn.processors.nlp',
 'fastnn.utils',
 'fastnn.utils.qa']

package_data = \
{'': ['*']}

install_requires = \
['coremltools>=4.0,<5.0',
 'jupyter>=1.0.0,<2.0.0',
 'jupyterlab>=2.2.9,<3.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'transformers>=3.0.0,<4.0.0',
 'wget>=3.2,<4.0']

extras_require = \
{'docs': ['mkdocs>=1.1.2,<2.0.0',
          'mkdocs-material>=6.1.5,<7.0.0',
          'mkautodoc>=0.1.0,<0.2.0'],
 'torch': ['torch>=1.0.0,<2.0.0', 'torchvision<1.0.0']}

setup_kwargs = {
    'name': 'fastnn',
    'version': '0.1.0',
    'description': 'A python library and framework for fast neural network computations.',
    'long_description': None,
    'author': 'Andrew Chang',
    'author_email': 'aychang995@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
