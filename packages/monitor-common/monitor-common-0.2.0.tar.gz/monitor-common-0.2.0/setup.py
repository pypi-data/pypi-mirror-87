# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monitor_common', 'monitor_common.mongodb']

package_data = \
{'': ['*']}

install_requires = \
['aenum>=2.2,<3.0', 'mongoengine>=0.18.2,<0.19.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses==0.7']}

setup_kwargs = {
    'name': 'monitor-common',
    'version': '0.2.0',
    'description': 'Common code used for the internet monitor app.',
    'long_description': '# Internet Monitor Common Code\n\nThis is a small library used by my internet monitor Python app. It provides the MongoDB integration as well as globally\nused classes and enums.\n\n## Installation\n\nTo install from PyPi run:\n```bash\npip install monitor-common\n```\n\n## Development and deployment\n\nSee the [Contribution guidelines for this project](CONTRIBUTING.md) for details on how to make changes to this library.\n',
    'author': 'George Blackburn',
    'author_email': 'g-a-b@hotmail.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/Malrig/monitor-common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
