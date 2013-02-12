"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import shlex
import subprocess

from os import listdir, path
from zipfile import error as BadZipFile
from zipfile import ZipFile

from django.core.exceptions import ValidationError

from settings import MAX_UPLOAD_SIZE, SCHEMA_PATH, XML_MIME_TYPES
from settings import ZIP_MIME_TYPES
from trendminer import UploadFormErrors
from utils import archive_extracted, file_on_disk, get_file_ext, get_tmp_path


def validate_extension(uploaded_file):
    if not (uploaded_file.name.lower().endswith('zip') or
            uploaded_file.name.lower().endswith('xml')):
        raise ValidationError(UploadFormErrors.EXTENSION)

def validate_size(uploaded_file):
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(UploadFormErrors.SIZE)

@file_on_disk
def validate_mime_type(uploaded_file):
    subproc = subprocess.Popen(
        'file --mime-type {}'.format(get_tmp_path( uploaded_file.name)),
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
                    raise ValidationError(UploadFormErrors.FILES_SCHEMA_CONFORMITY)
    elif file_type == '.xml':
        command = shlex.split(
            'xmllint --noout --schema "{0}" "{1}"'.format(
                SCHEMA_PATH, get_tmp_path(uploaded_file.name)))
        subproc = subprocess.Popen(command)
        if not subproc.wait() == 0:
            raise ValidationError(UploadFormErrors.XML_SCHEMA_CONFORMITY)
