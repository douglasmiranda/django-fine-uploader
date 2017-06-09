from django import forms
from django_fine_uploader import widgets


class FileFieldWithFineUploaderForm(forms.Form):
    """This form using the Fineuploader field as the upload field for FileField.
    """
    uploadfile = forms.FileField(widget=widgets.FineUploaderWidget)
