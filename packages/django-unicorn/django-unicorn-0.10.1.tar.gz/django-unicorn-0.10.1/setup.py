# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_unicorn',
 'django_unicorn.management.commands',
 'django_unicorn.templatetags']

package_data = \
{'': ['*'],
 'django_unicorn': ['static/js/*',
                    'static/js/morphdom/2.6.1/*',
                    'static/svg/*',
                    'templates/unicorn/*']}

install_requires = \
['beautifulsoup4>=4.8.0',
 'cachetools>=4.1.1,<5.0.0',
 'django>=3.0.0',
 'orjson>=3.2.1,<4.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'django-unicorn',
    'version': '0.10.1',
    'description': 'A magical full-stack framework for Django.',
    'long_description': '# django-unicorn\n\n![PyPI](https://img.shields.io/pypi/v/django-unicorn?color=blue&style=flat-square)\n\n![GitHub Release Date](https://img.shields.io/github/release-date/adamghill/django-unicorn?style=flat-square)\n\n<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->\n\n[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)\n\n<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\nThe magical fullstack framework for Django. ✨\n\n`django-unicorn` provides a way to use backend Django code and regular Django templates to create interactive experiences without investing in a separate frontend framework.\n\n## Why?\n\nBuilding server-side sites in Django with the ORM and template engine is so pleasant, but once you need more interactivity on the frontend, there is a lot more ambiguity. Should you build out an entire API in Django REST framework? Should you use React or Vue.js (or some) other frontend framework?\n\nIt seems like there should be an easier way to create interactive experiences.\n\n## A note\n\n`django-unicorn` is still beta and the API will likely change on the way to version 1.0.0. All efforts will be made to include an easy upgrade path. 1.0.0 will signify that the public API won\'t change until the next major release.\n\n# Detailed documentation\n\nhttps://www.django-unicorn.com\n\n# Developing\n\n1. `git clone git@github.com:adamghill/django-unicorn.git`\n1. `poetry install`\n1. `poetry run example/manage.py migrate`\n1. `poetry run example/manage.py runserver 0:8000`\n1. Go to `localhost:8000` in your browser\n1. To install in another project `pip install -e ../django-unicorn`\n\n## Run unittests\n\n1. `poetry run pytest`\n1. `npm run test`\n\n## Minify Javascript\n\n1. `npm install`\n1. `npm run build`\n\n## Bump version\n\n1. `npm run build`\n1. `poetry version major|minor|patch`\n1. Commit/tag/push version bump\n1. `poetry publish --build -r test`\n1. Make sure test package can be installed as expected (https://test.pypi.org/project/django-unicorn/)\n1. `poetry publish`\n1. Make sure live package can be installed as expected (https://pypi.org/project/django-unicorn/)\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://adamghill.com"><img src="https://avatars0.githubusercontent.com/u/317045?v=4" width="100px;" alt=""/><br /><sub><b>Adam Hill</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=adamghill" title="Code">💻</a> <a href="https://github.com/adamghill/django-unicorn/commits?author=adamghill" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://python3.ninja"><img src="https://avatars1.githubusercontent.com/u/44167?v=4" width="100px;" alt=""/><br /><sub><b>Andres Vargas</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=zodman" title="Code">💻</a></td>\n    <td align="center"><a href="http://iskra.ml"><img src="https://avatars3.githubusercontent.com/u/6555851?v=4" width="100px;" alt=""/><br /><sub><b>Eddy Ernesto del Valle Pino</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=edelvalle" title="Code">💻</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-enable -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'Adam Hill',
    'author_email': 'unicorn@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.django-unicorn.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
