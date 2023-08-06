# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['handcalcs']

package_data = \
{'': ['*'], 'handcalcs': ['templates/html/*', 'templates/latex/*']}

install_requires = \
['innerscope>=0.2.0,<0.3.0',
 'more-itertools>=8.5.0,<9.0.0',
 'nbconvert>=5.6.1,<6.0.0',
 'pyparsing>=2.4.7,<3.0.0']

setup_kwargs = {
    'name': 'handcalcs',
    'version': '1.2.0',
    'description': 'Python calculations in Jupyter as though you wrote them by hand.',
    'long_description': None,
    'author': 'Connor Ferster',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/connorferster/handcalcs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
