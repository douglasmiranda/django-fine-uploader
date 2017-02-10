# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views import generic

from .forms import FineUploaderUploadForm, FineUploaderUploadSuccessForm
from .fineuploader import ChunkedFineUploader
from . import settings


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
        return self.make_response({'success': True})

    def form_invalid(self, form):
        data = {'success': False, 'error': '%s' % repr(form.errors)}
        return self.make_response(data, status=400)
