# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wildwood']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.48',
 'numpy>=1.17',
 'scikit-learn>=0.22',
 'scipy>=1.3.2',
 'tqdm>=4.36']

setup_kwargs = {
    'name': 'wildwood',
    'version': '0.1',
    'description': 'scikit-learn compatible alternative random forests algorithms',
    'long_description': '# forest\nAdvanced random forest methods in Python\n',
    'author': 'Stéphane Gaïffas',
    'author_email': 'stephane.gaiffas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wildwood.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
