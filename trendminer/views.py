"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
import subprocess

from os import path
from xml.etree import ElementTree
from zipfile import ZipFile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as _login, logout as _logout
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from trendminer.settings import COMMIT_TAG, MAX_UPLOAD_SIZE, PERL_PATH
from trendminer.forms import UploadForm


def home(request):
    dictionary = {
      'title': 'TrendMiner Web Services',
      'commit_tag': COMMIT_TAG,
    }
    return render_to_response("home.html", dictionary,
      context_instance=RequestContext(request))


def login(request, template_name):
    """
    Renders login view by connecting to django.contrib.auth.views.
    """
    if request.user.username:
        dictionary = {
          'title': 'TrendMiner Web Services',
          'commit_tag': COMMIT_TAG,
          'message': 'You are already logged in as ' \
            ' <code>"{0}"</code>.'.format(request.user.username),
        }

        return render(request, 'home.html', dictionary)

    extra_context = {'commit_tag': COMMIT_TAG}
    return _login(request, template_name, extra_context=extra_context)


def logout(request, next_page):
    """
    Renders logout view by connecting to django.contrib.auth.views.
    """
    return _logout(request, next_page)


@login_required
def analyse(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            result, entities, add_info = _analyse(request.FILES['data'])
            message = 'Success!'
        else:
            result, entities, add_info = None, [], None
            message = form.errors['data']
    else:
        form = UploadForm()
        result = None
        entities = []
        add_info = None
        message = None

    dictionary = {
        'title': 'Trendminer Web Services',
        'commit_tag': COMMIT_TAG,
        'max_upload_size': MAX_UPLOAD_SIZE / (1024**2),
        'form': form,
        'result': result,
        'entities': entities,
        'add_info': add_info,
        'message': message,
        }
    return render_to_response(
        "analyse.html", dictionary,
        context_instance=RequestContext(request))


def _analyse(data):
    with open(path.join('/tmp', data.name), 'w') as destination:
        for chunk in data.chunks():
            destination.write(chunk)
    archive = ZipFile(path.join('/tmp', data.name), 'r')
    folder_name = path.splitext(data.name)[0]
    archive.extractall(path.join('/tmp', folder_name))
    command = 'perl -I {0} {1}'.format(
        PERL_PATH, path.join(PERL_PATH, 'om-xml.pl'))
    subprocess.call(
        command, cwd=path.join('/tmp', folder_name), shell=True)
    # Parse XML and serialize entities
    result = open(path.join('/tmp', folder_name, 'om.xml')).read()
    result_tree = ElementTree.fromstring(result)
    entities = sorted([
        (entity.find('name').text,
         entity.find('source_title').text,
         entity.find('ticker_string').text,
         entity.find('polarity').text)
        for entity in result_tree])
    add_info = open(
        path.join('/tmp', folder_name, 'pol_string.txt')).read()
    return result, entities, add_info
