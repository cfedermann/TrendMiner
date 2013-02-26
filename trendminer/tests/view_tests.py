"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import os
import shutil

from tempfile import gettempdir

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from settings import COMMIT_TAG

class ViewTest(TestCase):
    urls = 'trendminer.urls'

    def setUp(self):
        self.browser = Client()
        self.user = User.objects.create_user(
            username='trendminer-demo', password='trendminer-demo')

    def __check_status_code(self, response, expected_value=200):
        self.assertEquals(response.status_code, expected_value)

    def __check_template_used(self, response, expected_template):
        self.assertTemplateUsed(response, expected_template)

    def __check_context_var(self, response, var, expected_value):
        value = response.context[var]
        self.assertEquals(value, expected_value)

    def test_home_view(self):
        response = self.browser.get('/')
        self.__check_status_code(response)
        self.__check_template_used(response, 'home.html')
        self.__check_context_var(response, 'title', 'TrendMiner Web Services')
        self.__check_context_var(response, 'commit_tag', COMMIT_TAG)

    def test_login_view(self):
        response = self.browser.get('/login/')
        self.__check_status_code(response)
        self.__check_template_used(response, 'login.html')
        self.__check_context_var(response, 'commit_tag', COMMIT_TAG)
        response = self.browser.post(
            '/login/',
            {'username': self.user.username, 'password': 'trendminer-demo'},
            follow=True)
        self.__check_status_code(response)
        self.__check_context_var(response, 'commit_tag', COMMIT_TAG)
        response = self.browser.post(
            '/login/',
            {'username': self.user.username, 'password': 'trendminer-demo'},
            follow=True)
        self.__check_status_code(response)
        self.__check_context_var(response, 'title', 'TrendMiner Web Services')
        self.__check_context_var(response, 'commit_tag', COMMIT_TAG)
        self.__check_template_used(response, 'home.html')
        self.__check_context_var(
            response, 'message',
            'You are already logged in as <code>"trendminer-demo"</code>.')

    def test_logout_view(self):
        response = self.browser.get('/logout/')
        self.assertRedirects(response, '/')
        self.browser.login(
            username=self.user.username, password='trendminer-demo')
        response = self.browser.get('/logout/')
        self.assertRedirects(response, '/')

    def test_analyse_view(self):
        # GET request, not logged in
        response = self.browser.get('/analyse/')
        self.assertRedirects(response, '/login/?next=/analyse/')
        # GET request, logged in
        self.browser.login(
            username=self.user.username, password='trendminer-demo')
        response = self.browser.get('/analyse/')
        self.__check_status_code(response)
        self.__check_template_used(response, 'analyse.html')
        # GET request for results, non-existing request_id
        request_id = '2013-01-01_12-00-00_'
        response = self.browser.get('/analyse/{0}/1/'.format(request_id))
        self.__check_status_code(response, 404)
        self.__check_template_used(response, '404.html')
        # GET request for results, existing request_id
        folder = os.path.join(gettempdir(), request_id)
        os.mkdir(folder)
        with open(os.path.join(folder, 'om.xml'), 'w') as results:
            results.write(
                '<?xml version="1.0" encoding="UTF-8"?>\n' \
                    '<opinion>\n' \
                    '<entity>\n' \
                    '<name>XYZ</name>\n' \
                    '<source_name>NAME</source_name>\n' \
                    '<source_id>>XY2013010101234</source_id>\n' \
                    '<source_title>(ABC) title</source_title>\n' \
                    '<pub_date>\n' \
                    '<day>01</day>\n' \
                    '<month>01</month>\n' \
                    '<year>2013</year>\n' \
                    '</pub_date>\n' \
                    '<ticker_string>\n' \
                    'Foo (-23,00%), Bar (-42,00%)\n' \
                    '</ticker_string>\n' \
                    '<polarity>0</polarity>\n' \
                    '</entity>\n' \
                    '</opinion>\n')
        response = self.browser.get('/analyse/{0}/1/'.format(request_id))
        self.__check_status_code(response)
        self.__check_template_used(response, 'analyse.html')
        # GET request for results, existing request_id, page out-of-range
        response = self.browser.get('/analyse/{0}/100/'.format(request_id))
        self.assertRedirects(response, '/analyse/{0}/1/'.format(request_id))
        # GET request for results, existing request_id, invalid page value
        response = self.browser.get('/analyse/{0}/foo/'.format(request_id))
        self.__check_status_code(response, 404)
        self.__check_template_used(response, '404.html')
        shutil.rmtree(folder)
