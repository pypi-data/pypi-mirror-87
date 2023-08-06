# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['interdict']

package_data = \
{'': ['*']}

install_requires = \
['flatten-dict']

setup_kwargs = {
    'name': 'interdict',
    'version': '2020.11.0a1',
    'description': 'Dictionary filter',
    'long_description': '# interdict\nPython dictionary filter\n',
    'author': 'Shane R. Spencer',
    'author_email': '305301+whardier@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whardier/interdict',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
