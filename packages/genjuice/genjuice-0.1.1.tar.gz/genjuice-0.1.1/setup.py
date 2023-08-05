# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genjuice', 'genjuice.components']

package_data = \
{'': ['*']}

install_requires = \
['bleach>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'genjuice',
    'version': '0.1.1',
    'description': 'A lightweight, component-based HTML builder',
    'long_description': '# GenJuice\n\n<p align="center">\n    <img src="https://img.shields.io/pypi/l/genjuice?style=for-the-badge">\n    <img src="https://img.shields.io/pypi/pyversions/genjuice?style=for-the-badge">\n    <img src="https://img.shields.io/github/languages/code-size/docyx/genjuice?style=for-the-badge">\n    <img src="https://img.shields.io/github/issues-raw/docyx/genjuice?style=for-the-badge">\n</p>\n\n\nA lightweight, component-based HTML builder.\n\n```py\nfrom genjuice import Component\nfrom genjuice.components import Button\n\nclass FancyButton(Component):\n    def render(self):\n        return Button("Hello, world!").attr(onclick="alert(1)").render()\n```\n\n```py\n>>> FancyButton().render()\n"""\n<button onclick="alert(1)">Hello, world!</button>\n"""\n```\n\n## Installation\n\nGenJuice isn\'t quite ready for production yet. Feel free to mess around with it:\n\n```\npip install genjuice\n```\n\n## Why GenJuice?\n\n- The core functionality (`Component.render()`) is less than 30 lines long\n- On average, it\'s 2.2x faster than its counterparts (HTML builders/template engines such as Jinja)\n- You write your UI code in 100% Python (including CSS!)\n- A modern, intuitive API\n- ...and much more to come!\n\n## License\n\n[MIT](./LICENSE)\n',
    'author': 'docyx',
    'author_email': 'oliverxur@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/docyx/genjuice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
