"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@gmail.com>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import shlex
import subprocess

from os import listdir
from zipfile import error as BadZipFile
from zipfile import ZipFile

from django.core.exceptions import ValidationError

from trendminer.settings import ACCEPTED_FILE_TYPES, MAX_UPLOAD_SIZE
from trendminer.settings import SCHEMA_PATH, XML_MIME_TYPES, ZIP_MIME_TYPES
from trendminer import UploadFormErrors
from trendminer.utils import archive_extracted, file_on_disk, get_file_ext
from trendminer.utils import get_tmp_path


def validate_extension(uploaded_file):
    """
    Check if extension of uploaded file is listed in `ACCEPTED_FILE_TYPES`.
    """
    if not get_file_ext(uploaded_file.name.lower()) in ACCEPTED_FILE_TYPES:
        raise ValidationError(UploadFormErrors.EXTENSION)

def validate_size(uploaded_file):
    """
    Check if size of uploaded file exceeds maximum file size for
    uploads as defined by the `MAX_UPLOAD_SIZE` setting.
    """
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(UploadFormErrors.SIZE)

@file_on_disk
def validate_mime_type(uploaded_file):
    """
    Check MIME type of uploaded file and make sure it corresponds to
    the file's extension.

    This function uses the UNIX `file` command with the `--mime-type`
    option to obtain the MIME type of the uploaded file. It then
    checks to see if the MIME type corresponds to one of the types
    appropriate for the file's extension.
    """
    # pylint: disable-msg=E1101
    subproc = subprocess.Popen(
        'file --mime-type {}'.format(get_tmp_path(uploaded_file.name)),
        shell=True, stdout=subprocess.PIPE)
    mime_type = subproc.stdout.read().strip().split(': ')[-1]
    file_extension = get_file_ext(uploaded_file.name)
    if file_extension == '.zip' and not mime_type in ZIP_MIME_TYPES:
        raise ValidationError(
            UploadFormErrors.MIME_TYPE.format('.zip', mime_type))
    elif file_extension == '.xml' and not mime_type in XML_MIME_TYPES:
        raise ValidationError(UploadFormErrors.MIME_TYPE.format(
                '.xml', mime_type))

@file_on_disk
def validate_zip_integrity(uploaded_file):
    """
    If uploaded file is a .zip archive, check its integrity and the
    integrity of the files it contains.

    In case of a corrupted archive the `ZipFile` constructor raises
    IOError. To check the integrity of the files contained in the
    archive, the `ZipFile.testzip()` function is used.

    If the uploaded file appears to be a .zip archive (because its
    extension is `.zip`), but actually isn't, the `ZipFile`
    constructor raises `BadZipFile`. Because this case is covered by
    the MIME type validator, the function does not raise a
    ValidationError in this case.
    """
    if uploaded_file.name.endswith('zip'):
        corrupted_file = None
        try:
            archive = ZipFile(get_tmp_path(uploaded_file.name))
            corrupted_file = archive.testzip()
        except IOError:
            raise ValidationError(UploadFormErrors.ZIP_INTEGRITY)
        except BadZipFile:
            pass
        if corrupted_file:
            raise ValidationError(UploadFormErrors.FILES_INTEGRITY)

@file_on_disk
def validate_zip_contents(uploaded_file):
    """
    If uploaded file is a .zip archive, check if all of the files it
    contains are XML files.

    This function examines the extension of each file in the .zip
    archive to determine if it is an XML file. As of right now, it
    does not check MIME types.
    """
    contents = []
    if uploaded_file.name.endswith('zip'):
        try:
            archive = ZipFile(get_tmp_path(uploaded_file.name))
            contents = archive.namelist()
        except (IOError, BadZipFile):
            pass
        if any(not item.endswith('xml') for item in contents):
            raise ValidationError(UploadFormErrors.ZIP_CONTENTS)

@archive_extracted
@file_on_disk
def validate_xml_well_formedness(uploaded_file):
    """
    Check if XML files that are part of a single upload are
    well-formed.

    This function uses the `xmlwf` tool to determine if a given XML
    file is well-formed. The tool does not use standard return codes
    for representing the outcome of the check. Instead, if a file is
    well-formed, it simply outputs nothing. If it's not, xmlwf writes
    a description of the problem to standard output.
    """
    # pylint: disable-msg=E1101
    file_type = get_file_ext(uploaded_file.name)
    if file_type == '.zip' and uploaded_file.folder:
        for file_name in listdir(get_tmp_path(uploaded_file.folder)):
            if file_name.endswith('.xml') and not file_name == 'om.xml':
                command = shlex.split('xmlwf "{}"'.format(
                        get_tmp_path(uploaded_file.folder, file_name)))
                subproc = subprocess.Popen(command, stdout=subprocess.PIPE)
                error_msg = subproc.stdout.read()
                if error_msg:
                    raise ValidationError(
                        UploadFormErrors.FILES_WELLFORMEDNESS)
    elif file_type == '.xml':
        command = shlex.split('xmlwf "{}"'.format(
                get_tmp_path(uploaded_file.name)))
        subproc = subprocess.Popen(command, stdout=subprocess.PIPE)
        error_msg = subproc.stdout.read()
        if error_msg:
            raise ValidationError(UploadFormErrors.XML_WELLFORMEDNESS)

@archive_extracted
@file_on_disk
def validate_against_schema(uploaded_file):
    """
    Check if XML files that are part of a single upload validate
    against the TrendMiner XML schema.

    This function uses the `xmllint` tool to check if a given XML file
    conforms to the TrendMiner XML schema. The schema is defined in
    `<project-dir>/trendminer.xsd`. For any file that validates
    against the schema, the xmllint tool returns 0.
    """
    # pylint: disable-msg=E1101
    file_type = get_file_ext(uploaded_file.name)
    if file_type == '.zip' and uploaded_file.folder:
        for file_name in listdir(get_tmp_path(uploaded_file.folder)):
            if file_name.endswith('.xml') and not file_name == 'om.xml':
                command = shlex.split(
                    'xmllint --noout --schema "{0}" "{1}"'.format(
                        SCHEMA_PATH,
                        get_tmp_path(uploaded_file.folder, file_name)))
                subproc = subprocess.Popen(command)
                returncode = subproc.wait()
                if not returncode == 0:
                    raise ValidationError(
                        UploadFormErrors.FILES_SCHEMA_CONFORMITY)
    elif file_type == '.xml':
        command = shlex.split(
            'xmllint --noout --schema "{0}" "{1}"'.format(
                SCHEMA_PATH, get_tmp_path(uploaded_file.name)))
        subproc = subprocess.Popen(command)
        if not subproc.wait() == 0:
            raise ValidationError(UploadFormErrors.XML_SCHEMA_CONFORMITY)
