# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dummypygreet']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'dummypygreet',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Suresh Babu Jonathan',
    'author_email': 'Jonathan.SureshBabu-EE@infineon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
