import json

from django import forms
from django.urls import reverse


class FineUploaderWidget(forms.MultipleHiddenInput):
    template_name = 'django_fine_uploader/widget.html'

    def __init__(self, attrs=None, **kwargs):
        self.options = kwargs.pop('options', {})

        self.allow_delete = kwargs.pop('allow_delete', True)
        self.allow_retry = kwargs.pop('allow_retry', True)
        self.drop_label = kwargs.get('drop_label', 'Or just drag and drop file(s) here')
        self.upload_label = kwargs.get('upload_label', 'Select file(s)')
        self.delete_label = kwargs.pop('delete_label', 'Delete')
        self.retry_label = kwargs.pop('retry_label', 'Retry')
        self.pause_label = kwargs.pop('pause_label', 'Pause')
        self.continue_label = kwargs.pop('continue_label', 'Continue')
        self.close_label = kwargs.get('close_label', 'Close')
        self.yes_label = kwargs.get('yes_label', 'Yes')
        self.no_label = kwargs.get('no_label', 'No')
        self.ok_label = kwargs.get('ok_label', 'OK')
        self.cancel_label = kwargs.get('cancel_label', 'Cancel')

        self.include_js = kwargs.pop('include_js', True)
        self.include_css = kwargs.pop('include_css', True)
        super(FineUploaderWidget, self).__init__(attrs, **kwargs)
        self.type = 'hidden'

    def get_context(self, name, value, attrs):
        context = super(FineUploaderWidget, self).get_context(name, value, attrs)
        upload_url = reverse('django_fine_uploader:upload')
        options = {
            'request': {
                'endpoint': upload_url,
            },
            'deleteFile': {
                'enabled': True,
                'endpoint':  reverse('django_fine_uploader:delete'),
            },
            'chunking': {
                'enabled': True,
                'concurrent': {
                    'enabled': True
                },
                'success': {
                    'endpoint': '%s?done' % upload_url
                }
            }
        }
        options.update(self.options)
        context.update({
            'options': json.dumps(options),
            'allow_delete': self.allow_delete,
            'allow_retry': self.allow_retry,
            'drop_label': self.drop_label,
            'upload_label': self.upload_label,
            'delete_label': self.delete_label,
            'retry_label': self.retry_label,
            'pause_label': self.pause_label,
            'continue_label': self.continue_label,
            'close_label': self.close_label,
            'yes_label': self.yes_label,
            'no_label': self.no_label,
            'ok_label': self.ok_label,
            'cancel_label': self.cancel_label,
        })
        return context

    @property
    def media(self):
        kwargs = {}
        if self.include_js:
            kwargs['js'] = (
                'django_fine_uploader/js.cookie.min.js',
                'django_fine_uploader/fine-uploader.min.js',
            )
        if self.include_css:
            kwargs['css'] = {
                'all': ('django_fine_uploader/fine-uploader-gallery.min.css',)
            }
        return forms.Media(**kwargs)
