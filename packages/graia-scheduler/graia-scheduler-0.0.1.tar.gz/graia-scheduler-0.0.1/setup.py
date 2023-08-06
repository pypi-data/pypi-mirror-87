# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia', 'graia.scheduler']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=0.3.36,<0.4.0', 'graia-broadcast>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'graia-scheduler',
    'version': '0.0.1',
    'description': 'a scheduler for graia framework',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': '31543961+GreyElaina@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
