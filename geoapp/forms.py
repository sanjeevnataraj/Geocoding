from django import forms
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    file = forms.FileField(required=True)

    def clean(self):
        cleaned_data = super(UploadFileForm, self).clean()
        file_name = self.cleaned_data.get('file')
        if file_name:
            file_name = str(file_name)
            file_format = file_name.split(".")[1]
            if file_format != 'xlsx'and file_format != 'xls':
                self.add_error('file','Only xlsx format is accepted')