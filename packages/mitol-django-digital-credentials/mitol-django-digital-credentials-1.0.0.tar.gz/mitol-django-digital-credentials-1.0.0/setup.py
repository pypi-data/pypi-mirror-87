# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitol', 'mitol.digitalcredentials', 'mitol.digitalcredentials.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.12,<3.0.0',
 'django-oauth-toolkit>=1.2.0,<2.0.0',
 'djangorestframework>=3.9,<4.0',
 'mitol-django-common>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'mitol-django-digital-credentials',
    'version': '1.0.0',
    'description': 'Django application to support digital credentials',
    'long_description': None,
    'author': 'MIT Office of Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
