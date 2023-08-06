# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neutronics_pd']

package_data = \
{'': ['*']}

install_requires = \
['datetime>=4.3',
 'numpy>=1.18.1',
 'pandas>=1.0.1',
 'pathlib>=1.0.1',
 'xarray>=0.15.0']

setup_kwargs = {
    'name': 'neutronics-pd',
    'version': '0.1.0',
    'description': 'Python Library for neutronics output',
    'long_description': '# Neutronics Pandas\n[<img src="assets/neutronics_pandas2.png" width="300">](assets/neutronics_pandas2.png)',
    'author': 'gmariano',
    'author_email': 'giovanni.mariano@enea.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
