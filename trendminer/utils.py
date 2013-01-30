"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import re

from os import path
from zipfile import ZipFile


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
