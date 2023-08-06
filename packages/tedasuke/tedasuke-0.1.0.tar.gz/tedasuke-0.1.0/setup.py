# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tedasuke']
setup_kwargs = {
    'name': 'tedasuke',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ucpr',
    'author_email': 'contact@ucpr.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
