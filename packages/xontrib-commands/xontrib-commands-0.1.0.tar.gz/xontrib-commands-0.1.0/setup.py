# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "4.0"': ['arger>=1.0.0,<2.0.0',
                                                         'rich']}

setup_kwargs = {
    'name': 'xontrib-commands',
    'version': '0.1.0',
    'description': 'Useful xonsh-shell commands/alias functions',
    'long_description': '<p align="center">\nUseful xonsh-shell commands/alias functions\n</p>\n\n<p align="center">\nIf you like the idea click ⭐ on the repo and stay tuned.\n</p>\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-commands\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-commands\n```\n\n## Usage\n\n``` bash\nxontrib load commands\n\n```\n\n## Commands\n\n### 1. reload-mods\n![](./docs/2020-12-02-14-30-47.png)\n\n### 2. report-key-bindggs\n![](./docs/2020-12-02-14-30-17.png)\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-commands',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
