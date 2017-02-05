=====
Usage
=====

To use django_fine_uploader in a project, add it to your `INSTALLED_APPS`:

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
