# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamkeeper', 'streamkeeper.services']

package_data = \
{'': ['*']}

install_requires = \
['python-daemon>=2.2.4,<3.0.0',
 'python-pushover>=0.4,<0.5',
 'streamlink>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['streamkeeper = streamkeeper.streamkeeper:main']}

setup_kwargs = {
    'name': 'streamkeeper',
    'version': '2.0.1',
    'description': 'Keep those livestreams to watch whenever you want',
    'long_description': "# Streamkeeper\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nWatches configured youtube channels and will automatically download any live streams the youtube channel posts, then this can convert to a particular video format. Optionally you can get notified over pushover.\n\n## Quickstart\n\nFor now copy config.ini.sample to config.ini and fill in following the TODO comments.\n\n* `pip install streamkeeper`\n* `streamkeeper process /path/to/config.ini` - This runs streamkeeper in the foreground.\n* `streamkeeper daemon config.ini` - This runs streamkeeper in the background(where config.ini is in the current folder).\n\nNote: The script requires [ffmpeg](https://ffmpeg.org/) if you wish to enable conversions. So this needs to be installed with it's executable in the current path.\n\n## Development\n\n### Setup\n\n* `make setup`\n* `make start` or `make daemon` to background it\n\n### Testing\n\n* `make test`\n\n### Publishing\n\n* `make build`\n* `make publish`\n",
    'author': 'Shane Dowling',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
