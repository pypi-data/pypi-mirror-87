# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hsc_instructions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hsc-instructions',
    'version': '0.5.0',
    'description': 'Instruction encoding and decoding for the hsc (name TBD) isa',
    'long_description': 'Python library implementing decoding instructions into Instruction objects and encoding Instruction objects into binary instructions.\n',
    'author': 'Bolun Thompson',
    'author_email': 'abolunthompson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HomebrewSiliconClub/Processor',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
