# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gen3',
 'gen3.tools',
 'gen3.tools.bundle',
 'gen3.tools.indexing',
 'gen3.tools.metadata']

package_data = \
{'': ['*'], 'gen3.tools.indexing': ['tmp/*']}

install_requires = \
['aiohttp',
 'backoff',
 'click',
 'drsclient<1.0.0',
 'indexclient>=1.6.2',
 'pandas',
 'pypfb<1.0.0',
 'requests']

entry_points = \
{'console_scripts': ['gen3 = gen3.cli:main']}

setup_kwargs = {
    'name': 'gen3',
    'version': '3.0.0',
    'description': 'Gen3 CLI and Python SDK',
    'long_description': None,
    'author': 'Center for Translational Data Science at the University of Chicago',
    'author_email': 'support@datacommons.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gen3.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
