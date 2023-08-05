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
    'version': '0.0.1',
    'description': 'Easy progress bar for streamlit based on the awesome streamlit.progress and tqdm',
    'long_description': '# stqdm\n![Tests](https://github.com/Wirg/stqdm/workflows/Tests/badge.svg)\n\nstqdm is the simplest way to handle a progress bar in streamlit.\n\n![demo gif](assets/demo.gif)\n\n## How to install\n\n```sh\npip install stqdm\n```\n\n## How to use\n\nYou can find some examples in `examples/`\n\n### Use stqdm in main\n```python\nfrom time import sleep\nfrom stqdm import stqdm\n\nfor _ in stqdm(range(50)):\n    sleep(0.5)\n```\n\n### Use stqdm in sidebar\n```python\nfrom time import sleep\nimport streamlit as st\nfrom stqdm import stqdm\n\nfor _ in stqdm(range(50), st_container=st.sidebar):\n    sleep(0.5)\n```\n',
    'author': 'Wirg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Wirg/stqdm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
