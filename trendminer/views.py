"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as _login, logout as _logout
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from trendminer.settings import COMMIT_TAG


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
def analyze(request):
    dictionary = {
        'title': 'Trendminer Web Services',
        'commit_tag': COMMIT_TAG,
        }
    return render_to_response(
        "analyze.html", dictionary,
        context_instance=RequestContext(request))
