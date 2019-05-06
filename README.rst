django-httpbench
================

HTTP load testing tools for Django.
Like an apache bench but requests are sent from authenticated users without having to know their password.

Installation
------------

django-httpbench requires python 3.6 or later and Django 2.0 or later.

.. code-block:: console

   $ python3 -m pip install djangohttpbench


https://pypi.org/project/djangohttpbench/

Usage
-----

HeaderAuthBackend
~~~~~~~~~~~~~~~~~

Django authentication backend that allows one to login without having to know their password.
This backend is useful for testing scenarios.

.. code-block:: python

    HTTP_BENCH_USERNAME_KEY = "X-USERNAME"  # default: X-USERNAME

    INSTALLED_APPS += [
        'httpbench.apps.HttpbenchConfig',
    ]

    MIDDLEWARE += [
        'httpbench.middlewares.HeaderAuthMiddleware',
    ]

    AUTHENTICATION_BACKENDS += [
        'httpbench.backends.UsernameBackend',
    ]


.. code-block:: console

   $ curl -H 'X-USERNAME: c-bata' https://localhost:8000/path/to/page/require/auth


``httpbench`` management command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`httpbench` management command acts like an apache bench but requests are sent from authenticated users.

.. code-block:: console

   $ python3 manage.py httpbench -n 1000 -c 50 \
   > --username c-bata \
   > https://localhost:8000/
   Response time:
     mean: 3.862 secs
     min: 1.173 secs
     max: 11.097 secs
   Status:
     2xx: 1000
     3xx: 0
     4xx: 0
     5xx: 0
     fail: 0

Development
-----------

* lint: ``tox -e flake8`` or ``flake8``
* test: ``tox -e py37`` or ``python setup.py test --settings=test_settings``

License
-------

This software is licensed under the MIT License (See `LICENSE <./LICENSE>`_ ).
