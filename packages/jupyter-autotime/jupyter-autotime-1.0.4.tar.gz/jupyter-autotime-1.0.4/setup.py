# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autotime']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=6,<8']

setup_kwargs = {
    'name': 'jupyter-autotime',
    'version': '1.0.4',
    'description': 'Display elapsed time on Jupyter.',
    'long_description': '# jupyter-autotime\n\nDisplay elapsed time on Jupyter.\n\n![Demo](demo.gif)\n\n## Getting start\n\n1. Install\n   * On shell.\n\n      ```sh\n      pip install jupyter-autotime\n      ```\n\n   * On Jupyter.\n\n      ```python\n      !pip install jupyter-autotime\n      ```\n\n1. Enable autotime\n\n   ```python\n   # Only JupyterLab\n   import autotime\n   autotime.LAB = True\n   ```\n\n   ```python\n   %load_ext autotime\n   ```\n\n## Other usage\n\n```python\n# Reload.\n%reload_ext autotime\n\n# Disable.\n%unload_ext autotime\n```\n\n## Development\n\n* Requirements: poetry, pyenv\n\n```sh\npoetry install\n\npoetry publish\n\npip install --no-cache-dir --upgrade jupyter-autotime\n```\n',
    'author': 'Takeru Saito',
    'author_email': 'takelushi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/takelushi/jupyter-autotime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
