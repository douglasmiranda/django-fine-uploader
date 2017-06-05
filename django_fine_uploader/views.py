# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import generic

import shutil
from os.path import join

from .forms import FineUploaderUploadForm, FineUploaderUploadSuccessForm
from .fineuploader import ChunkedFineUploader
from . import settings
from . import utils


class FineUploaderView(generic.FormView):
    """View which will handle all upload requests sent by Fine Uploader.
    You can use it with simple uploads:
    http://docs.fineuploader.com/branch/master/endpoint_handlers/traditional.html
    Chunked uploads:
    http://docs.fineuploader.com/branch/master/features/chunking.html
    Or Concurrent Chunked Uploads:
    http://docs.fineuploader.com/branch/master/features/concurrent-chunking.html
    """
    http_method_names = ('post', )
    # Specific Django Fine Uploader configuration.
    form_class_upload = FineUploaderUploadForm
    form_class_upload_success = FineUploaderUploadSuccessForm

    @property
    def concurrent(self):
        return settings.CONCURRENT_UPLOADS

    @property
    def chunks_done(self):
        # http://docs.fineuploader.com/api/options.html#chunking.success.endpoint
        return self.chunks_done_param_name in self.request.GET

    @property
    def chunks_done_param_name(self):
        return settings.CHUNKS_DONE_PARAM_NAME

    def process_upload(self, form):
        self.upload = ChunkedFineUploader(form.cleaned_data, self.concurrent)
        if self.upload.concurrent and self.chunks_done:
            self.upload.combine_chunks()
        else:
            self.upload.save()

    def make_response(self, data, **kwargs):
        return JsonResponse(data, **kwargs)

    def get_form(self, form_class=None):
        if self.chunks_done:
            form_class = self.form_class_upload_success
        else:
            form_class = self.form_class_upload
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        self.process_upload(form)
        return self.make_response({
            'success': True,
            'path': self.upload.real_path,
        })

    def form_invalid(self, form):
        data = {'success': False, 'error': '%s' % repr(form.errors)}
        return self.make_response(data, status=400)


class FineUploaderDeleteView(generic.View):
    """
    View that handle file deletion.

    From the FineUploader docs:

    If you have enabled this feature, you will need to handle the
    corresponding DELETE or POST requests server-side. The method is
    configurable via the method property of the deleteFile option.

    For DELETE requests, the UUID of the file to delete will be specified as
    the last element of the URI path. Any custom parameters specified will be
    added to the query string. For POST requests, the UUID is sent as a
    "qquuid" parameter, and a "_method" parameter is sent with a value of
    "DELETE". All POST request parameters are sent in the request payload.

    Success of the request will depend solely on the response code.
    Acceptable response codes that indicate success are 200, 202, and 204 for
    DELETE requests and 200-204 for POST requests.
    """
    http_method_names = [u'post', u'delete']

    def post(self, request, *args, **kwargs):
        """
        Handle the file deletion via a POST HTTP request.
        """
        uuid = request.POST.get('qquuid')
        if request.POST.get('_method') != 'DELETE' or not uuid:
            raise HttpResponseBadRequest()
        kwargs.update({'uuid': uuid})
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Handle the file deletion via a DELETE HTTP request.
        """
        file_storage = utils.import_class(settings.FILE_STORAGE)()
        uuid = kwargs.get('uuid')
        path = join(settings.UPLOAD_DIR, uuid)
        if file_storage.exists(path):
            full_path = file_storage.path(path)
            try:
                shutil.rmtree(full_path)
                return JsonResponse({'success': True, 'uuid': uuid})
            except (OSError, PermissionError):
                pass
        raise HttpResponseBadRequest()
