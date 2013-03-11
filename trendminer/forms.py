"""
Project: TrendMiner Demo Web Services
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
    """
    This class defines the form for uploading user data to Trendminer
    for analysis.

    Each class attribute represents a separate input field of the
    form.
    """
    data = forms.FileField(
        validators=[
            validate_extension, validate_size,
            validate_mime_type, validate_zip_integrity,
            validate_zip_contents, validate_xml_well_formedness,
            validate_against_schema])

    def clean_data(self):
        """
        Perform custom clean-up steps on `data` field of the
        UploadForm.

        When calling the `is_valid()` method on a form, Django
        performs a series of default steps for validating and cleaning
        user submitted data. This method adds custom logic to the
        clean-up process for the `data` field: The name of the user
        submitted file is altered to make sure that it conforms to a
        format that won't confuse any subsequent subprocess calls.
        """
        data = self.cleaned_data['data']
        data.name = sanitize_file_name(data.name)
        return data
