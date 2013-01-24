"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django import forms

from trendminer.validators import validate_zip_format, validate_size
from trendminer.validators import validate_mime_type, validate_zip_integrity
from trendminer.validators import validate_zip_contents

class UploadForm(forms.Form):
    data = forms.FileField(
        validators=[
            validate_zip_format, validate_size,
            validate_mime_type, validate_zip_integrity,
            validate_zip_contents])
