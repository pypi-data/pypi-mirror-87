# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genjuice', 'genjuice.components', 'genjuice.components._gen']

package_data = \
{'': ['*']}

install_requires = \
['bleach>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'genjuice',
    'version': '0.1.0',
    'description': 'A lightweight, component-based HTML builder',
    'long_description': '# GenJuice\n\nA lightweight, component-based HTML builder\n\n```py\nfrom genjuice import Component\nfrom genjuice.components import Button\n\n\nclass FancyButton(Component):\n    def render(self):\n        return Button(\n            "Hello, world!"\n        ).render()\n```\n',
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
