# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prose', 'prose.migrations']

package_data = \
{'': ['*'], 'prose': ['static/prose/*', 'templates/prose/forms/widgets/*']}

install_requires = \
['django>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'django-prose',
    'version': '0.3.0',
    'description': 'Wonderful rich text for Django',
    'long_description': '# Django Prose\n\nWonderful rich-text editing in Django.\n\n## Install\n\n```console\npip install django-prose\n```\n\n\n---\n\n<p align="center">\n  <i>Built with ❤️ in Athens, Greece.</i>\n</p>\n',
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@sourcelair.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/parisk/django-prose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
