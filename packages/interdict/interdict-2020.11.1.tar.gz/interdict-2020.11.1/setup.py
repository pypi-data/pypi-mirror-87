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
    'version': '2020.11.1',
    'description': 'Dictionary filter',
    'long_description': "# interdict\nPython dictionary filter\n\n# Installation\n\n`pip install interdict`\n\n# Examples\n\n## Default (inclusion False)\n\n```python\n>>> from interdict import filter_obj\n>>> obj = {'name': 'shane', 'job': {'salary': 1000000, 'role': 'master of universe'}}\n>>> filter = {'name': True, 'job': {'role': True}}\n>>> filter_obj(obj, filter)\n{'name': 'shane', 'job': {'role': 'master of universe'}}\n```\n\n## Inclusive (a.k.a. TMI)\n\n```python\n>>> filter_obj(obj, filter, default=True)\n{'name': 'shane', 'job': {'salary': 1000000, 'role': 'master of universe'}}\n```\n\n## Inclusive with better filter\n\n```python\n>>> filter = {'job': {'salary': False}}\n>>> filter_obj(obj, filter, default=True)\n{'name': 'shane', 'job': {'role': 'master of universe'}}\n```\n\n## Stacked filters\n\n```python\n>>> obj = {'name': 'shane', 'job': {'salary': 1000000, 'role': {'title': 'master of universe', 'reality': 'dumpster fire starter'}}}\n>>> filter_1 = {'name': False}\n>>> filter_2 = {'job': {'salary': False, 'role': {'reality': False}}}\n>>> filter_obj(obj, [filter_1, filter_2], default=True)\n{'job': {'role': {'title': 'master of universe'}}}\n```\n",
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
