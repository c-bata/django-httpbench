django-httpbench
================

HTTP load testing tools for Django.
Like an apache bench but requests are sent from authenticated users without having to know their password.

Usage
-----

Requirements:

Supported python versions are python 3.6 or later.

* django (>= 2.0)
* requests

Installation

.. code-block:: console

   $ python3 -m pip install django-httpbench

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


.. code-block:: console

   $ curl -H 'X-USERNAME: c-bata' https://localhost:8000/path/to/page/require/auth


'httpbench' management command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`httpbench` management command acts like an apache bench but requests are sent from authenticated users.

.. code-block:: console

   $ python manage.py httpbench \
   > --username c-bata \
   > --url https://localhost:8000/

Contributing
------------

Flake8
~~~~~~

.. code-block:: console

   $ flake8


Run unittests
~~~~~~~~~~~~~

.. code-block:: console

   $ DJANGO_SETTINGS_MODULE=test_settings python -m django test


License
~~~~~~~

This software is licensed under the MIT License (See `LICENSE <./LICENSE>`_ ).
