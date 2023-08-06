# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_generation_pytest', 'auto_generation_pytest.combination']

package_data = \
{'': ['*'], 'auto_generation_pytest': ['demo/*']}

install_requires = \
['allpairspy>=2.5.0,<3.0.0',
 'allure-pytest>=2.8.16,<3.0.0',
 'grpcio-tools>=1.30.0,<2.0.0',
 'grpcio>=1.30.0,<2.0.0',
 'pytest>=5.4.3,<6.0.0',
 'pytest_dependency',
 'python-dotenv>=0.14.0,<0.15.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['mat = auto_generation_pytest.cli:main']}

setup_kwargs = {
    'name': 'auto-generation-pytest',
    'version': '1.0.4',
    'description': 'auto_generation_pytest',
    'long_description': None,
    'author': 'moku27',
    'author_email': 'xieshi@forchange.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
