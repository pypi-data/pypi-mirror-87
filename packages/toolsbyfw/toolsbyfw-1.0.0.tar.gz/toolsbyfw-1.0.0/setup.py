# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['toolsbyfw']
setup_kwargs = {
    'name': 'toolsbyfw',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'FolwWolf',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
