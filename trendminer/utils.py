"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import re

from os import path
from zipfile import ZipFile

from settings import ACCEPTED_FILE_TYPES


def sanitize_file_name(name):
    return re.sub('[\(\)\[\]]', '', name.lower().replace(' ', '_'))

def write_file(uploaded_file, path):
    with open(path, 'w') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def extract_archive(file_path):
    archive = ZipFile(file_path, 'r')
    folder_name = path.splitext(file_path)[0]
    archive.extractall(path.join('/tmp', folder_name))
    return folder_name

def file_on_disk(func):
    def wrapper(*args, **kwargs):
        uploaded_file = args[0]
        uploaded_file.name = sanitize_file_name(uploaded_file.name)
        file_path = path.join('/tmp', uploaded_file.name)
        file_extension = path.splitext(file_path)[1]
        if file_extension in ACCEPTED_FILE_TYPES and not \
                path.exists(file_path):
            write_file(uploaded_file, path.join('/tmp', uploaded_file.name))
        return func(*args, **kwargs)
    return wrapper
