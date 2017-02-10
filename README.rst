=============================
Django Fine Uploader
=============================

Simple, Chunked and Concurrent uploads with Django + Fine Uploader

This is an alpha version.

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

And finally your html file:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link href="https://cdnjs.cloudflare.com/ajax/libs/file-uploader/5.13.0/fine-uploader-gallery.min.css" rel="stylesheet">
      <script type="text/template" id="qq-template">
        <div class="qq-uploader-selector qq-uploader qq-gallery" qq-drop-area-text="Drop files here">
          <div class="qq-total-progress-bar-container-selector qq-total-progress-bar-container">
            <div role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" class="qq-total-progress-bar-selector qq-progress-bar qq-total-progress-bar"></div>
          </div>
          <div class="qq-upload-drop-area-selector qq-upload-drop-area" qq-hide-dropzone>
            <span class="qq-upload-drop-area-text-selector"></span>
          </div>
          <div class="qq-upload-button-selector qq-upload-button">
            <div>Upload a file</div>
          </div>
          <span class="qq-drop-processing-selector qq-drop-processing">
            <span>Processing dropped files...</span>
            <span class="qq-drop-processing-spinner-selector qq-drop-processing-spinner"></span>
          </span>
          <ul class="qq-upload-list-selector qq-upload-list" role="region" aria-live="polite" aria-relevant="additions removals">
            <li>
              <span role="status" class="qq-upload-status-text-selector qq-upload-status-text"></span>
              <div class="qq-progress-bar-container-selector qq-progress-bar-container">
                <div role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" class="qq-progress-bar-selector qq-progress-bar"></div>
              </div>
              <span class="qq-upload-spinner-selector qq-upload-spinner"></span>
              <div class="qq-thumbnail-wrapper">
                <img class="qq-thumbnail-selector" qq-max-size="120" qq-server-scale>
              </div>
              <button type="button" class="qq-upload-cancel-selector qq-upload-cancel">X</button>
              <button type="button" class="qq-upload-retry-selector qq-upload-retry">
                <span class="qq-btn qq-retry-icon" aria-label="Retry"></span>
                  Retry
              </button>

              <div class="qq-file-info">
                <div class="qq-file-name">
                  <span class="qq-upload-file-selector qq-upload-file"></span>
                  <span class="qq-edit-filename-icon-selector qq-btn qq-edit-filename-icon" aria-label="Edit filename"></span>
                </div>
                <input class="qq-edit-filename-selector qq-edit-filename" tabindex="0" type="text">
                <span class="qq-upload-size-selector qq-upload-size"></span>
                <button type="button" class="qq-btn qq-upload-delete-selector qq-upload-delete">
                  <span class="qq-btn qq-delete-icon" aria-label="Delete"></span>
                </button>
                <button type="button" class="qq-btn qq-upload-pause-selector qq-upload-pause">
                  <span class="qq-btn qq-pause-icon" aria-label="Pause"></span>
                </button>
                <button type="button" class="qq-btn qq-upload-continue-selector qq-upload-continue">
                  <span class="qq-btn qq-continue-icon" aria-label="Continue"></span>
                </button>
              </div>
            </li>
          </ul>

          <dialog class="qq-alert-dialog-selector">
            <div class="qq-dialog-message-selector"></div>
            <div class="qq-dialog-buttons">
              <button type="button" class="qq-cancel-button-selector">Close</button>
            </div>
          </dialog>

          <dialog class="qq-confirm-dialog-selector">
            <div class="qq-dialog-message-selector"></div>
            <div class="qq-dialog-buttons">
              <button type="button" class="qq-cancel-button-selector">No</button>
              <button type="button" class="qq-ok-button-selector">Yes</button>
            </div>
          </dialog>

          <dialog class="qq-prompt-dialog-selector">
            <div class="qq-dialog-message-selector"></div>
            <input type="text">
            <div class="qq-dialog-buttons">
              <button type="button" class="qq-cancel-button-selector">Cancel</button>
              <button type="button" class="qq-ok-button-selector">Ok</button>
            </div>
          </dialog>
        </div>
      </script>
      <title>Django Fine Uploader</title>
    </head>
    <body>
      <div id="default-concurrent-chunked-uploader"></div>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/file-uploader/5.13.0/fine-uploader.min.js"></script>
      <!-- Cookies.js, so we can get the CSRFToken cookie -->
      <script src="https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.1.3/js.cookie.min.js" charset="utf-8"></script>
      <script>
        var default_concurrent_chunked_uploader = new qq.FineUploader({
          debug: true,
          element: document.getElementById('default-concurrent-chunked-uploader'),
          request: {
            endpoint: '{% url 'django_fine_uploader:upload' %}',
            customHeaders: {
              'X-CSRFToken': Cookies.get('csrftoken')
            }
          },
          chunking: {
            enabled: true,
            concurrent: {
                enabled: true
            },
            success: {
              endpoint: '{% url 'django_fine_uploader:upload' %}?done'
            }
          }
        });
      </script>
    </body>
    </html>

Features
--------

* Simple Upload
* Chunked Upload
* Concurrent Chunked Upload
* Ready to use upload endpoint
* Easy extend FineUploaderView (FormView)
* Or create your custom view and use the Django Fine Uploader handler

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
