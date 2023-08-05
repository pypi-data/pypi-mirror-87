# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stqdm']

package_data = \
{'': ['*']}

install_requires = \
['streamlit>=0.71.0,<0.72.0', 'tqdm>=4.54.0,<5.0.0']

setup_kwargs = {
    'name': 'stqdm',
    'version': '0.0.0',
    'description': 'Easy progress bar for streamlit based on the awesome streamlit.progress and tqdm',
    'long_description': None,
    'author': 'Wirg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
