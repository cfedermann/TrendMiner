"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import os
import re
import shutil
import time

from datetime import datetime
from os import path
from zipfile import ZipFile
from zipfile import error as BadZipFile

from settings import ACCEPTED_FILE_TYPES, TMP_PATH, URL_PREFIX


def prefix_url(url):
    """
    Add url prefix defined in `settings.py` to url.
    """
    if not url or url == '/':
        return '/{}/'.format(URL_PREFIX.strip('/'))
    else:
        return '/{0}/{1}/'.format(URL_PREFIX.strip('/'), url.strip('/'))

def sanitize_file_name(name):
    """
    Lowercase file name; replace spaces with underscores and remove
    parentheses and square brackets.
    """
    return re.sub('[\(\)\[\]]', '', name.lower().replace(' ', '_'))

def add_timestamp_prefix(file_name):
    """
    Add timestamp of the form `YYYY-MM-DD_hh-mm-ss_` to file name.

    If file name already contains a timestamp of this format, simply
    return the file name as is.
    """
    if not starts_with_timestamp(file_name):
        return datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d_%H-%M-%S') + '_{}'.format(file_name)
    else:
        return file_name

def starts_with_timestamp(file_name):
    """
    Check if file name starts with timestamp of the form
    `YYYY-MM-DD_hh-mm-ss_`.
    """
    return re.match('\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_', file_name)

def get_tmp_path(*args):
    """
    Return absolute path of file or folder in `TMP_PATH`.

    `TMP_PATH` is defined in `settings.py`. The function wraps a call
    to `os.path.join` and therefore supports multiple arguments.
    """
    return path.join(TMP_PATH, *args)

def get_file_ext(file_name):
    """
    Return extension part of file name.

    This method is a thin wrapper around `os.path.splitext`: If
    supplied file name ends with an extension, the `splitext` function
    returns it as a string containing a leading dot. If it doesn't,
    the function returns an empty string.
    """
    return path.splitext(file_name)[1]

def remove_upload(file_name):
    """
    Completely remove a file upload from the upload directory.

    If the upload is an archive of type `.zip`, this function also
    checks for a corresponding folder holding any files extracted from
    the archive, and deletes it if it exists.
    """
    file_path = get_tmp_path(file_name.lower())
    if os.path.exists(file_path):
        os.remove(file_path)
        if get_file_ext(file_path) == '.zip':
            output_folder = os.path.splitext(file_path)[0]
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)

def store_upload(uploaded_file, path):
    """
    Write uploaded file to destination supplied in the `path`
    parameter.

    The uploaded file needs to be of type `django.core.files.File` or
    `django.core.files.uploadedfile.UploadedFile`.
    """
    with open(path, 'w') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def extract_archive(file_path):
    """
    Extract .zip archive to folder in the same directory as the
    archive, and return the name of the extracted folder.

    The function expects the `file_path` parameter to supply the
    absolute path to the archive to be extracted.
    """
    folder_name = path.splitext(file_path)[0]
    try:
        archive = ZipFile(file_path, 'r')
        archive.extractall(get_tmp_path(folder_name))
    except (IOError, BadZipFile):
        folder_name = None
    return folder_name

def file_on_disk(func):
    """
    Decorator for functions that operate on a file upload and need the
    uploaded file to be stored in the local file system.
    """
    def wrapper(*args, **kwargs):
        """
        Store uploaded file in upload directory.

        Only store files of accepted types, and skip rewriting the
        file to disk if it already exists.
        """
        uploaded_file = args[0]
        file_extension = get_file_ext(uploaded_file.name)
        uploaded_file.name = add_timestamp_prefix(
            sanitize_file_name(uploaded_file.name))
        file_path = get_tmp_path(uploaded_file.name)
        if file_extension in ACCEPTED_FILE_TYPES and not \
                path.exists(file_path):
            store_upload(uploaded_file, file_path)
        return func(*args, **kwargs)
    return wrapper

def archive_extracted(func):
    """
    Decorator for functions that operate on a file upload and need
    contents of a .zip archive to be extracted into a dedicated folder
    in the local file system.
    """
    def wrapper(*args, **kwargs):
        """
        If uploaded file is a .zip archive, extract its contents to
        the local file system.

        The name of the folder to hold the extracted files corresponds
        to the name of the archive, with the `.zip` extension removed.
        """
        uploaded_file = args[0]
        file_extension = get_file_ext(uploaded_file.name)
        if file_extension == '.zip':
            folder = extract_archive(get_tmp_path(uploaded_file.name))
            uploaded_file.folder = folder
        return func(*args, **kwargs)
    return wrapper
