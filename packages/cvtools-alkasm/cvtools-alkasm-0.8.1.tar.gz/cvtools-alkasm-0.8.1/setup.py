# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvtools', 'cvtools.extras']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python!=4.2.0.32']

setup_kwargs = {
    'name': 'cvtools-alkasm',
    'version': '0.8.1',
    'description': 'Utilities for computer vision in Python',
    'long_description': "A collection of useful utilities for computer vision in Python. \n\nMany of these functions came directly out of Stack Overflow answers that I've provided to add some otherwise missing functionality in OpenCV. Others come from me repeating something I tend to do often.\n\nThere's no core API that isn't prone to breaking on a whim.\n\nOpenCV is not installed along with this package, you must install it yourself before using `cvtools`.\n\n## Install\n    \n```sh\npip install cvtools-alkasm\n```\n",
    'author': 'Alexander Reynolds',
    'author_email': 'ar@reynoldsalexander.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alkasm/cvtools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
