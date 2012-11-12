"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django import forms


class UploadForm(forms.Form):
    data = forms.FileField()
