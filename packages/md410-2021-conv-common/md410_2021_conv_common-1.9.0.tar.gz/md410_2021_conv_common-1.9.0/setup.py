# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['md410_2021_conv_common']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'psycopg2-binary>=2.8.4,<3.0.0',
 'sqlalchemy>=1.3.12,<2.0.0']

setup_kwargs = {
    'name': 'md410-2021-conv-common',
    'version': '1.9.0',
    'description': 'Common libraries for applications related to the 2020 and 2021 Lions MD410 Conventions',
    'long_description': '# Introduction\n\nCommon libraries for applications related to the 2020 and [2021 Lions Multiple District 410 Conventions](https://www.lionsconvention2021.co.za/).\n\n# Associated Applications\n\nSee [this Gitlab group](https://gitlab.com/md410_2021_conv) for associated applications.\n',
    'author': 'Kim van Wyk',
    'author_email': 'vanwykk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/md410_2021_conv/md410_2021_conv_common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
