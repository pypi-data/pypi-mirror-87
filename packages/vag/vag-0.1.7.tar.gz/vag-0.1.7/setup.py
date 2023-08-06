# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vag', 'vag.console', 'vag.console.commands', 'vag.utils']

package_data = \
{'': ['*'], 'vag': ['scripts/build/*', 'scripts/instance/*']}

install_requires = \
['Click>=7.1.2,<8.0.0', 'jinja2>=2.11.2,<3.0.0', 'untangle>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['vag = vag.console.application:main']}

setup_kwargs = {
    'name': 'vag',
    'version': '0.1.7',
    'description': 'vagrant utility cli tool',
    'long_description': '# vag\nvag is a command line utility tool for vagrant\n\n## Github repo\n[vag](https://github.com/7onetella/vag)\n\n## Documentation\n[read the docs](https://vag.readthedocs.io/en/latest/index.html)\n\n## Installation\n```bash\n$ pip install vag\n```\n\n## Development\nlocal vag installation\n```bash\n$ rm -rf dist/*\n$ poetry install\n$ poetry build\n$ pip uninstall -y vag\n$ pip install dist/*.whl\n```\n\nedit and run \n```bash\n$ poetry run vag instance list\n```\n\n',
    'author': 'Seven Tella',
    'author_email': '7onetella@gmail.com',
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
