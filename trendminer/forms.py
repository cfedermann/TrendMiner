"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django import forms

from utils import sanitize_file_name
from validators import validate_extension, validate_size
from validators import validate_mime_type, validate_zip_integrity
from validators import validate_zip_contents

class UploadForm(forms.Form):
    data = forms.FileField(
        validators=[
            validate_extension, validate_size,
            validate_mime_type, validate_zip_integrity,
            validate_zip_contents])

    def clean_data(self):
        data = self.cleaned_data['data']
        data.name = sanitize_file_name(data.name)
        return data
