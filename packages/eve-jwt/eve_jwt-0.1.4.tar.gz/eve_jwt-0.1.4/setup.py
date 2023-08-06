# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eve_jwt', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['Authlib==0.14.3',
 'eve>=1.1.4,<2.0.0',
 'expiringdict>=1.2.1,<2.0.0',
 'flask>=1.1.2,<2.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'eve-jwt',
    'version': '0.1.4',
    'description': 'Top-level package for eve-jwt.',
    'long_description': '=======\neve-jwt\n=======\n\n\n.. image:: https://img.shields.io/pypi/v/eve_jwt.svg\n        :target: https://pypi.python.org/pypi/eve_jwt\n\n.. image:: https://img.shields.io/travis/jmosbacher/eve_jwt.svg\n        :target: https://travis-ci.com/jmosbacher/eve_jwt\n\n.. image:: https://readthedocs.org/projects/eve-jwt/badge/?version=latest\n        :target: https://eve-jwt.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\nEve JWT auth for asymmetric encryption. Adapted from eve-auth-jwt which handles symmetric encryption shcemes.\n\n\nUsage\n-----\n\n.. code-block:: python\n\n        from eve_jwt import JWTAuth\n        from eve import Eve\n\n        auth = JWTAuth(key_url="https://YOUR-OAUTH-SERVER/certs/")\n\n        app = Eve(auth=auth)\n\n\n* Free software: MIT\n* Documentation: https://eve-jwt.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/eve_jwt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
