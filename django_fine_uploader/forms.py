from django import forms


class FineUploaderUploadForm(forms.Form):
    """This form represents a basic request from Fine Uploader.
    The required fields will **always** be sent, the other fields are optional
    based on your setup.

    Extend this if you want to add custom parameters in the body of the POST
    request.
    """
    qqfile = forms.FileField()
    qquuid = forms.CharField()
    qqfilename = forms.CharField()
    qqpartindex = forms.IntegerField(required=False)
    qqchunksize = forms.IntegerField(required=False)
    qqtotalparts = forms.IntegerField(required=False)
    qqtotalfilesize = forms.IntegerField(required=False)
    qqpartbyteoffset = forms.IntegerField(required=False)


class FineUploaderUploadSuccessForm(forms.Form):
    """This form represents a request from Fine Uploader when you enabled
    concurrent chunked uploads.

    In this case you have to set a success.endpoint on fineuploader client
    configuration.
    http://docs.fineuploader.com/branch/master/api/options.html#chunking.success.endpoint
    """
    qquuid = forms.CharField()
    qqfilename = forms.CharField()
    qqtotalparts = forms.IntegerField()
    qqtotalfilesize = forms.IntegerField(required=False)
