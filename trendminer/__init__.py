"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <t.krones@coli.uni-saarland.de>
"""

from settings import ACCEPTED_FILE_TYPES, MAX_UPLOAD_SIZE

class UploadFormErrors(object):
    EXTENSION = 'Upload must be in {} format.'.format(
        ' or '.join(ACCEPTED_FILE_TYPES))
    SIZE = 'Upload too large. The current limit is {}MB.'.format(
        MAX_UPLOAD_SIZE/(1024**2))
    MIME_TYPE = 'File appears to be in {0} format, but it is not ' \
        '(MIME-type: {1}).'
    ZIP_INTEGRITY = 'Archive is corrupted.'
    FILES_INTEGRITY = 'Archive contains corrupted files.'
    ZIP_CONTENTS = 'Archive contains files that are not in .xml format.'
    FILES_WELLFORMEDNESS = 'Archive contains XML files that are not' \
        'well-formed.'
    XML_WELLFORMEDNESS = 'XML file is not well-formed.'
    FILES_SCHEMA_CONFORMITY = 'Archive contains XML files that do not ' \
        'validate against the TrendMiner XML schema.'
    XML_SCHEMA_CONFORMITY = 'XML file does not validate against TrendMiner ' \
        'XML schema.'
