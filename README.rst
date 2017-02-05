=============================
django_fine_uploader
=============================

.. image:: https://badge.fury.io/py/django-fine-uploader.svg
    :target: https://badge.fury.io/py/django-fine-uploader

.. image:: https://travis-ci.org/douglasmiranda/django-fine-uploader.svg?branch=master
    :target: https://travis-ci.org/douglasmiranda/django-fine-uploader

.. image:: https://codecov.io/gh/douglasmiranda/django-fine-uploader/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/douglasmiranda/django-fine-uploader

Simple, Chunked and Concurrent uploads with Django + Fine Uploader

Documentation
-------------

The full documentation is at https://django-fine-uploader.readthedocs.io.

Quickstart
----------

Install django_fine_uploader::

    pip install django-fine-uploader

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_fine_uploader.apps.DjangoFineUploaderConfig',
        ...
    )

Add django_fine_uploader's URL patterns:

.. code-block:: python

    from django_fine_uploader import urls as django_fine_uploader_urls


    urlpatterns = [
        ...
        url(r'^', include(django_fine_uploader_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
