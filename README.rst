=============================
Django Fine Uploader
=============================

Simple, Chunked and Concurrent uploads with Django_ + `Fine Uploader`_

.. _Django: https://www.djangoproject.com
.. _`Fine Uploader`: http://fineuploader.com

This is an alpha version.

We have a example_ project. Just `git clone` the django-fine-uploader repository and follow the instructions.

.. _example: https://github.com/douglasmiranda/django-fine-uploader/tree/master/example

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

    urlpatterns = [
        ...
        url(r'^fine-uploader/', include('django_fine_uploader.urls', namespace='django_fine_uploader')),
        ...
    ]

And finally your html file: copy from `this gist`_, lots of html to put on our README.

.. _`this gist`: https://gist.github.com/douglasmiranda/77da9c801e0cf83357ba51a639372768

Features
--------

* Simple Upload
* Chunked Upload
* Concurrent Chunked Upload
* `Ready to use upload endpoint`_
* `Easy extend FineUploaderView`_ (FormView)
* Or create your custom view and use the Django Fine Uploader handler

.. _`Ready to use upload endpoint`: https://github.com/douglasmiranda/django-fine-uploader/blob/master/django_fine_uploader/fineuploader.py
.. _`Easy extend FineUploaderView`: https://github.com/douglasmiranda/django-fine-uploader/blob/master/django_fine_uploader/views.py

TODO
----

* Tests, we need tests
* Docs
* Test with some File Storages

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

Fineuploader: http://fineuploader.com
