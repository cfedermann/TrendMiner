"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django import forms

from trendminer.validators import validate_zip_format, validate_size

class UploadForm(forms.Form):
    data = forms.FileField(
        validators=[validate_zip_format, validate_size])
