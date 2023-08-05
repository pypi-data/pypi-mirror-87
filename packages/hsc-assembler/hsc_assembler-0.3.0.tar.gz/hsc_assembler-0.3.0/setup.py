# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hsc_assembler']

package_data = \
{'': ['*']}

install_requires = \
['hsc-instructions>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['hsc_assembler = hsc_assembler.main:cli']}

setup_kwargs = {
    'name': 'hsc-assembler',
    'version': '0.3.0',
    'description': 'Assembler for the hsc (name TBD) ISA (https://github.com/HomebrewSiliconClub/Processor)',
    'long_description': 'Assembler for this project.\n\nThis uses the black auto formatter for code formatting\n\n# Usage\n\nTo use this, either use the assembler.sh script which requires docker or install this from pypi.\n\nTo install the pypi version, run `pip3 install hsc_assembler`.\n\n\n',
    'author': 'Bolun Thompson',
    'author_email': 'abolunthompson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HomebrewSiliconClub/Processor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
