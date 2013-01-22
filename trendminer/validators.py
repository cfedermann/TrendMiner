"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

from django.core.exceptions import ValidationError
from settings import MAX_UPLOAD_SIZE

def validate_zip_format(uploaded_file):
    if not (uploaded_file.name.lower().endswith('zip') or
            uploaded_file.name.lower().endswith('xml')):
        raise ValidationError(
            'Upload must be in .zip or .xml format.')

def validate_size(uploaded_file):
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(
            'Upload too large. The current limit is {}MB.'.format(
                MAX_UPLOAD_SIZE/(1024**2)))
