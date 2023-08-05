# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upscript']

package_data = \
{'': ['*']}

install_requires = \
['distlib']

entry_points = \
{'console_scripts': ['upscript = upscript:main']}

setup_kwargs = {
    'name': 'upscript',
    'version': '0.1.0',
    'description': 'Installs and updates python scripts for you',
    'long_description': None,
    'author': 'xppt',
    'author_email': '21246102+xppt@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
