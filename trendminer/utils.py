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
    if not url or url == '/':
        return '/{}/'.format(URL_PREFIX.strip('/'))
    else:
        return '/{0}/{1}/'.format(URL_PREFIX.strip('/'), url.strip('/'))

def sanitize_file_name(name):
    return re.sub('[\(\)\[\]]', '', name.lower().replace(' ', '_'))

def add_timestamp_prefix(file_name):
    if not starts_with_timestamp(file_name):
        return datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d_%H-%M-%S') + '_{}'.format(file_name)
    else:
        return file_name

def starts_with_timestamp(file_name):
    return re.match('\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_', file_name)

def get_tmp_path(*args):
    return path.join(TMP_PATH, *args)

def get_file_ext(file_name):
    return path.splitext(file_name)[1]

def remove_upload(file_name):
    file_path = get_tmp_path(file_name.lower())
    if os.path.exists(file_path):
        os.remove(file_path)
        if get_file_ext(file_path) == '.zip':
            output_folder = os.path.splitext(file_path)[0]
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)

def store_upload(uploaded_file, path):
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
        uploaded_file.name = add_timestamp_prefix(
            sanitize_file_name(uploaded_file.name))
        file_path = get_tmp_path(uploaded_file.name)
        if file_extension in ACCEPTED_FILE_TYPES and not \
                path.exists(file_path):
            store_upload(uploaded_file, file_path)
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
