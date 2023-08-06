=======
eve-jwt
=======


.. image:: https://img.shields.io/pypi/v/eve_jwt.svg
        :target: https://pypi.python.org/pypi/eve_jwt

.. image:: https://img.shields.io/travis/jmosbacher/eve_jwt.svg
        :target: https://travis-ci.com/jmosbacher/eve_jwt

.. image:: https://readthedocs.org/projects/eve-jwt/badge/?version=latest
        :target: https://eve-jwt.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Eve JWT auth for asymmetric encryption. Adapted from eve-auth-jwt which handles symmetric encryption shcemes.


Usage
-----

.. code-block:: python

        from eve_jwt import JWTAuth
        from eve import Eve

        auth = JWTAuth(key_url="https://YOUR-OAUTH-SERVER/certs/")

        app = Eve(auth=auth)


* Free software: MIT
* Documentation: https://eve-jwt.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage
