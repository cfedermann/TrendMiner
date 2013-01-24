"""
Project: ACCURAT Demo Translation Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import re

def sanitize_file_name(name):
    return re.sub('[\(\)\[\]]', '', name.lower().replace(' ', '_'))
