# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hesiod', 'hesiod.cfgparse', 'hesiod.ui', 'hesiod.ui.tui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'npyscreen>=4.10.5,<5.0.0']

setup_kwargs = {
    'name': 'hesiod',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Luca De Luigi',
    'author_email': 'lucadeluigi91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
