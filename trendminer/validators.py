"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import subprocess

from os import listdir, path
from zipfile import error as BadZipFile
from zipfile import ZipFile

from django.core.exceptions import ValidationError

from settings import MAX_UPLOAD_SIZE, XML_MIME_TYPES, ZIP_MIME_TYPES
from utils import extract_archive, sanitize_file_name, write_file


def validate_extension(uploaded_file):
    if not (uploaded_file.name.lower().endswith('zip') or
            uploaded_file.name.lower().endswith('xml')):
        raise ValidationError(
            'Upload must be in .zip or .xml format.')

def validate_size(uploaded_file):
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(
            'Upload too large. The current limit is {}MB.'.format(
                MAX_UPLOAD_SIZE/(1024**2)))

def validate_mime_type(uploaded_file):
    sanitized_file_name = sanitize_file_name(uploaded_file.name)
    file_extension = path.splitext(sanitized_file_name)[1]
    if file_extension == '.zip' or file_extension == '.xml':
        write_file(uploaded_file, path.join('/tmp', sanitized_file_name))
        subproc = subprocess.Popen(
            'file --mime-type {}'.format(
                path.join('/tmp', sanitized_file_name)),
            shell=True, stdout=subprocess.PIPE)
        mime_type = subproc.stdout.read().strip().split(': ')[-1]
        if file_extension == '.zip' and not mime_type in ZIP_MIME_TYPES:
            raise ValidationError(
                'File appears to be in .zip format, but it is not ' \
                    '(MIME-type: {}).'.format(mime_type))
        elif file_extension == '.xml' and not mime_type in XML_MIME_TYPES:
            raise ValidationError(
                'File appears to be in .xml format, but it is not ' \
                    '(MIME-type: {}).'.format(mime_type))

def validate_zip_integrity(uploaded_file):
    sanitized_file_name = sanitize_file_name(uploaded_file.name)
    if sanitized_file_name.endswith('zip'):
        corrupted_file = None
        try:
            archive = ZipFile(path.join('/tmp', sanitized_file_name))
            corrupted_file = archive.testzip()
        except IOError:
            raise ValidationError(
                'Archive is corrupted')
        except BadZipFile:
            pass
        if corrupted_file:
            raise ValidationError('Archive contains corrupted files')

def validate_zip_contents(uploaded_file):
    sanitized_file_name = sanitize_file_name(uploaded_file.name)
    contents = []
    if sanitized_file_name.endswith('zip'):
        try:
            archive = ZipFile(path.join('/tmp', sanitized_file_name))
            contents = archive.namelist()
        except (IOError, BadZipFile):
            pass
        if any(not item.endswith('xml') for item in contents):
            raise ValidationError(
                'Archive contains files that are not in XML format')

def validate_xml_well_formedness(uploaded_file):
    file_path = path.join('/tmp', sanitize_file_name(uploaded_file.name))
    file_type = path.splitext(file_path)[1]
    if file_type in ('.zip', '.xml') and not path.exists(file_path):
        write_file(uploaded_file, file_path)
    if file_type == '.zip':
        try:
            folder_name = extract_archive(file_path)
        except (IOError, BadZipFile):
            return
        for file_name in listdir(path.join('/tmp', folder_name)):
            sanitized_file_name = sanitize_file_name(file_name)
            if sanitized_file_name.endswith('.xml'):
                subproc = subprocess.Popen(
                    'xmlwf {}'.format(
                        path.join('/tmp', folder_name, sanitized_file_name)),
                    shell=True, stdout=subprocess.PIPE)
                error_msg = subproc.stdout.read()
                if error_msg:
                    raise ValidationError(
                        'Archive contains XML files that are not ' \
                            'well-formed')
    elif file_type == '.xml':
        subproc = subprocess.Popen(
            'xmlwf {}'.format(file_path), shell=True, stdout=subprocess.PIPE)
        error_msg = subproc.stdout.read()
        if error_msg:
            raise ValidationError('XML file is not well-formed')
