# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mds_test_package_2020']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'mds-test-package-2020',
    'version': '0.1.0',
    'description': 'some description',
    'long_description': None,
    'author': 'Mark Dunne',
    'author_email': 'markdunne@improbable.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
