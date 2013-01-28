"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django import forms

from utils import sanitize_file_name
from validators import validate_extension, validate_size
from validators import validate_mime_type, validate_zip_integrity
from validators import validate_zip_contents, validate_xml_well_formedness
from validators import validate_against_schema

class UploadForm(forms.Form):
    data = forms.FileField(
        validators=[
            validate_extension, validate_size,
            validate_mime_type, validate_zip_integrity,
            validate_zip_contents, validate_xml_well_formedness,
            validate_against_schema])

    def clean_data(self):
        data = self.cleaned_data['data']
        data.name = sanitize_file_name(data.name)
        return data
