"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import subprocess

from os import path
from xml.etree import ElementTree

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as _login, logout as _logout
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext

from settings import COMMIT_TAG, ENTITIES_PER_PAGE, MAX_UPLOAD_SIZE, PERL_PATH
from forms import UploadForm
from utils import archive_extracted, file_on_disk, get_file_ext, get_tmp_path


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
            '<code>"{0}"</code>.'.format(request.user.username),
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
def analyse(request, request_id=None, page=None):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            request_id = path.splitext(request.FILES['data'].name)[0]
            entities = _analyse(request.FILES['data'])
            paginator = Paginator(entities, ENTITIES_PER_PAGE)
            entities = paginator.page(1)
            message = 'Success!'
        else:
            entities = []
            message = form.errors['data']
    else:
        form = UploadForm()
        message = None
        if request_id and page:
            try:
                entities = parse_results(request_id)
            except IOError:
                raise Http404
            paginator = Paginator(entities, ENTITIES_PER_PAGE)
            try:
                entities = paginator.page(page)
            except EmptyPage:
                return redirect('results', request_id=request_id, page=1)
        else:
            entities = []

    dictionary = {
        'title': 'Trendminer Web Services',
        'commit_tag': COMMIT_TAG,
        'max_upload_size': MAX_UPLOAD_SIZE / (1024**2),
        'form': form,
        'message': message,
        'rid': request_id,
        'entities': entities,
        }
    return render_to_response(
        "analyse.html", dictionary,
        context_instance=RequestContext(request))


@archive_extracted
@file_on_disk
def _analyse(data):
    file_type = get_file_ext(data.name)
    if file_type == '.zip':
        command = 'perl -I {0} {1}'.format(
            PERL_PATH, path.join(PERL_PATH, 'om-xml.pl'))
        subprocess.call(
            command, cwd=get_tmp_path(data.folder), shell=True)
        entities = parse_results(data.folder)
    elif file_type == '.xml':
        entities = []
    return entities


def parse_results(request_id):
    result = open(get_tmp_path(request_id, 'om.xml')).read()
    result_tree = ElementTree.fromstring(result)
    entities = sorted([
            {'attributes': [entity.find('name').text,
                            entity.find('source_title').text,
                            entity.find('ticker_string').text],
             'polarity': entity.find('polarity').text,
             'polarity_range': range(int(entity.find('polarity').text))}
            for entity in result_tree])
    return entities
