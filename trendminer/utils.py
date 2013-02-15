"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import re
import time

from datetime import datetime
from os import path
from zipfile import ZipFile
from zipfile import error as BadZipFile

from settings import ACCEPTED_FILE_TYPES, TESTFILES_PATH, TMP_PATH


def sanitize_file_name(name):
    return re.sub('[\(\)\[\]]', '', name.lower().replace(' ', '_'))

def create_unique_file_name(file_name):
    if not starts_with_timestamp(file_name):
        return datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d_%H-%M-%S') + '_{}'.format(file_name)
    else:
        return file_name

def starts_with_timestamp(file_name):
    return re.match('\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}', file_name)

def get_tmp_path(*args):
    return path.join(TMP_PATH, *args)

def get_file_ext(file_name):
    return path.splitext(file_name)[1]

def get_test_file(file_name):
    flag = 'rb' if not get_file_ext(file_name) == '.xml' else 'r'
    return open(
        path.join(TESTFILES_PATH, file_name), flag)

def write_file(uploaded_file, path):
    with open(path, 'w') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def extract_archive(file_path):
    folder_name = path.splitext(file_path)[0]
    try:
        archive = ZipFile(file_path, 'r')
        archive.extractall(get_tmp_path(folder_name))
    except (IOError, BadZipFile):
        folder_name = None
    return folder_name

def file_on_disk(func):
    def wrapper(*args, **kwargs):
        uploaded_file = args[0]
        file_extension = get_file_ext(uploaded_file.name)
        uploaded_file.name = create_unique_file_name(
            sanitize_file_name(uploaded_file.name))
        file_path = get_tmp_path(uploaded_file.name)
        if file_extension in ACCEPTED_FILE_TYPES and not \
                path.exists(file_path):
            write_file(uploaded_file, file_path)
        return func(*args, **kwargs)
    return wrapper

def archive_extracted(func):
    def wrapper(*args, **kwargs):
        uploaded_file = args[0]
        file_extension = get_file_ext(uploaded_file.name)
        if file_extension == '.zip':
            folder = extract_archive(get_tmp_path(uploaded_file.name))
            uploaded_file.folder = folder
        return func(*args, **kwargs)
    return wrapper
