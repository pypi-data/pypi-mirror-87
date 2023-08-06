# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia',
 'graia.broadcast',
 'graia.broadcast.abstract',
 'graia.broadcast.abstract.interfaces',
 'graia.broadcast.builtin',
 'graia.broadcast.entities',
 'graia.broadcast.entities.signatures',
 'graia.broadcast.interfaces',
 'graia.broadcast.interrupt']

package_data = \
{'': ['*']}

install_requires = \
['iterwrapper>=0.1.2,<0.2.0', 'pydantic>=1.5.1,<1.7.1']

setup_kwargs = {
    'name': 'graia-broadcast',
    'version': '0.5.3',
    'description': 'a highly customizable, elegantly designed event system based on asyncio',
    'long_description': None,
    'author': 'Chenwe_i_lin',
    'author_email': 'Chenwe_i_lin@outlook.com',
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
