# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ihsan', 'ihsan.sdl']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'rich>=9.2.0,<10.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ihsan = ihsan.manage:app']}

setup_kwargs = {
    'name': 'ihsan',
    'version': '0.0.4',
    'description': 'Behold Ihsan Project',
    'long_description': "> ## 🛠 Status: In Development\n> Ihsan is currently in development. So we encourage you to use it and give us your feedback, but there are things that haven't been finalized yet and you can expect some changes.\n>\n> See the list of Known Issues and TODOs, below, for updates.\n\n\n## Overview\n\nBehold Ihsan Project\n\n\n## Installation\n\n```shell script\npoetry add ihsan\n\n```\n\nor\n\n```shell script\npip install ihsan\n\n```\n",
    'author': 'Mohamed Nesredin',
    'author_email': 'm.n.kaizen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mohamed-Kaizen/ihsan/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
