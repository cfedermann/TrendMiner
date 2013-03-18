"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@gmail.com>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import os
import shutil

from tempfile import gettempdir

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from settings import COMMIT_TAG

class ViewTest(TestCase):
    """
    This class provides tests for the view layer of the TrendMiner
    Demo Web Service.

    Each individual view function defined in `views.py` is tested
    using a single method of this class. Test functions are named
    after the view function they test. They are prefixed with `test_`.
    The `setUpClass` method sets up the test environment and is called
    once before any of the individual tests are run. The `setUp`
    method performs additional set up steps and is run before each
    individual test.

    To keep tests in this class from breaking when changing the
    `ROOT_URLCONF` setting in `settings.py`, the `urls` variable
    specifies which URLconf to use for the duration of executing the
    test suite, as documented here:

    https://docs.djangoproject.com/en/1.4/topics/testing/#urlconf-configuration
    """
    urls = 'trendminer.urls'

    @classmethod
    def setUpClass(cls):
        """
        Obtain URLs of relevant views.
        """
        cls.home_url = reverse('home')
        cls.login_url = reverse('trendminer.views.login')
        cls.logout_url = reverse('trendminer.views.logout')
        cls.analyse_url = reverse('analyse')

    def setUp(self):
        """
        Launch a browser instance to use for sending requests to
        TrendMiner and create test user in the test DB.
        """
        self.browser = Client()
        self.user = User.objects.create_user(
            username='trendminer-demo', password='trendminer-demo')

    def __result_url(self, request_id, page):
        """
        Build URL for browsing paginated results associated with a
        given request ID.

        For valid `page` values, this method uses the utility function
        `django.core.urlresolvers.reverse` to obtain the results URL
        for the given request ID and page. In any other case, it has
        to build the URL manually using string formatting. The reason
        for this is that the `reverse` function will not find a
        matching URL if the page value does not match the regular
        expression defined for this parameter in `urls.py`.
        """
        if type(page) == int:
            return reverse('results', args=[request_id, page])
        else:
            return '{0}{1}/{2}/'.format(self.analyse_url, request_id, page)

    def __check_status_code(self, response, expected_value=200):
        """
        Compare status code of a given response with the expected
        value.
        """
        self.assertEquals(response.status_code, expected_value)

    def __check_template_used(self, response, expected_template):
        """
        Check if a given response renders the appropriate template.
        """
        self.assertTemplateUsed(response, expected_template)

    def __check_context_var(self, response, var, expected_value):
        """
        Check if the value of a specific variable matches the expected
        value in the response context of the given response.
        """
        value = response.context[var]
        self.assertEquals(value, expected_value)

    def test_home_view(self):
        """
        To test the `home` view, this method first performs a GET
        request to the corresponding URL. It then checks if

        - the response's status code is 200, signaling that the
          request was successful
        - the appropriate template (`home.html`) was used for the
          response
        - the `title` and `commit_tag` context variables are set to
          the correct values.
        """
        response = self.browser.get(self.home_url)
        self.__check_status_code(response)
        self.__check_template_used(response, 'home.html')
        self.__check_context_var(response, 'title', 'TrendMiner Web Services')
        self.__check_context_var(response, 'commit_tag', COMMIT_TAG)

    def test_login_view(self):
        """
        To test the `login` view, this method performs a simple GET
        request and two POST requests to the corresponding URL. The
        first POST request sends login data consisting of user name
        and password to the login URL. The second POST request
        re-sends the same login data without logging out beforehand.
        In each case, the `login` view is expected to return a
        redirect to the `home` view. For the second POST request, we
        additionally expect the response to contain an appropriate
        alert message.

        For each request this method checks the status code of the
        response (the expected value is 200 for successful requests),
        as well as the template used by the view function to render
        the response. Additionally, it checks if

        - values of `title` and `commit_tag` variables are set
          correctly (GET request)
        - request context contains a user object whose `username`
          attribute is equal to the test user's user name (1st POST
          request)
        - value of the `message` variable is set correctly (2nd POST
          request)

        Note that as the `login` view uses
        `django.contrib.auth.views.login` to handle user
        authentication and only adds a minimal amount of custom logic,
        this method does not cover cases of unsuccessful
        authentication.
        """
        # GET request, not logged in
        response = self.browser.get(self.login_url)
        self.__check_status_code(response)
        self.__check_template_used(response, 'login.html')
        self.__check_context_var(response, 'title', 'TrendMiner Web Services')
        self.__check_context_var(response, 'commit_tag', COMMIT_TAG)
        # POST request with login data
        response = self.browser.post(
            self.login_url,
            {'username': self.user.username, 'password': 'trendminer-demo'},
            follow=True)
        self.__check_status_code(response)
        self.__check_template_used(response, 'home.html')
        username = response.context['user'].username
        self.assertEquals(username, self.user.username)
        # POST request with same login data
        response = self.browser.post(
            self.login_url,
            {'username': self.user.username, 'password': 'trendminer-demo'},
            follow=True)
        self.__check_status_code(response)
        self.__check_template_used(response, 'home.html')
        self.__check_context_var(
            response, 'message',
            'You are already logged in as <code>"trendminer-demo"</code>.')

    def test_logout_view(self):
        """
        To test the `logout view`, this method performs two GET
        requests to the corresponding URL. The first request is issued
        before the test user is logged in. The second request is
        issued after logging in the test user. In both cases, the
        `logout` view is expected to return a redirect to the `home`
        view.
        """
        # GET request, not logged in
        response = self.browser.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
        # GET request, logged in
        self.browser.login(
            username=self.user.username, password='trendminer-demo')
        response = self.browser.get(self.logout_url)
        self.assertRedirects(response, self.home_url)

    def test_analyse_view(self):
        """
        To test the `analyse` view, this method performs a series of
        GET requests to the corresponding URL. They are listed below,
        along with the expected results the method checks for. Note
        that as the `validator_tests.py` module provides extensive
        tests for POSTing data to the analyse view, these cases are
        not covered here.

        (1) Simple GET request, not logged in
            - redirect to `login` view, with `next` parameter set to
              URL of `analyse` view

        (2) Simple GET request, logged in
            - status code: 200
            - template used: `analyse.html`

        (3) GET request for non-existing results
            - status code: 404
            - template used: `404.html`

        (4) GET request for existing results
            - status code: 200
            - template used: `analyse.html`

        (5) GET request for existing results, page out of range
            - redirect to `analyse` view, with the page parameter
              changed to 1

        (6) GET request for existing results, invalid page value:
            - status code: 404
            - template used: `404.html`
        """
        # GET request, not logged in
        response = self.browser.get(self.analyse_url)
        self.assertRedirects(response, '{0}?next={1}'.format(
                self.login_url, self.analyse_url))
        # GET request, logged in
        self.browser.login(
            username=self.user.username, password='trendminer-demo')
        response = self.browser.get(self.analyse_url)
        self.__check_status_code(response)
        self.__check_template_used(response, 'analyse.html')
        # GET request for results, non-existing request_id
        request_id, page = '2013-01-01_12-00-00_', 1
        response = self.browser.get(self.__result_url(request_id, page))
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
        response = self.browser.get(self.__result_url(request_id, page))
        self.__check_status_code(response)
        self.__check_template_used(response, 'analyse.html')
        # GET request for results, existing request_id, page out-of-range
        page = 100
        response = self.browser.get(self.__result_url(request_id, page))
        self.assertRedirects(response, self.__result_url(request_id, page=1))
        # GET request for results, existing request_id, invalid page value
        page = 'foo'
        response = self.browser.get(self.__result_url(request_id, page))
        self.__check_status_code(response, 404)
        self.__check_template_used(response, '404.html')
        # Clean up
        shutil.rmtree(folder)
