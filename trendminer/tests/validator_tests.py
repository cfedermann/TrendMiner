from os import path

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from settings import TESTFILES_PATH


class ValidatorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='trendminer-demo', password='trendminer-demo')
        self.browser = Client()
        self.browser.login(
            username=self.user.username, password='trendminer-demo')

    def tearDown(self):
        self.browser.logout()

    def test_ext_validator(self):
        testfile = open(
            path.join(TESTFILES_PATH, 'trendminer-logo-final.png'), 'rb')
        response = self.browser.post('/analyse/', {'data': testfile})
        self.assertFormError(
            response, form='form', field='data',
            errors='Upload must be in .zip or .xml format.')

    def test_size_validator(self):
        testzip = open(path.join(TESTFILES_PATH, 'large.zip'), 'rb')
        response = self.browser.post('/analyse/', {'data': testzip})
        self.assertFormError(
            response, form='form', field='data',
            errors='Upload too large. The current limit is 5MB.')
        testxml = open(path.join(TESTFILES_PATH, 'large.xml'))
        response = self.browser.post('/analyse/', {'data': testxml})
        self.assertFormError(
            response, form='form', field='data',
            errors='Upload too large. The current limit is 5MB.')

    def test_mime_type_validator(self):
        testzip = open(path.join(TESTFILES_PATH, 'fake.zip'), 'rb')
        response = self.browser.post('/analyse/', {'data': testzip})
        self.assertFormError(
            response, form='form', field='data',
            errors='File appears to be in .zip format, but it is not ' \
            '(MIME-type: text/plain).')
        testxml = open(path.join(TESTFILES_PATH, 'fake.xml'))
        response = self.browser.post('/analyse/', {'data': testxml})
        self.assertFormError(
            response, form='form', field='data',
            errors=['File appears to be in .xml format, but it is not ' \
                        '(MIME-type: application/zip).',
                    'XML file is not well-formed',
                    'XML file does not validate against TrendMiner ' \
                        'XML Schema'])

    def test_zip_integrity_validator(self):
        testfile = open(path.join(TESTFILES_PATH, 'corrupt.zip'), 'rb')
        response = self.browser.post('/analyse/', {'data': testfile})
        self.assertFormError(
            response, form='form', field='data',
            errors='Archive is corrupted')

    def test_zip_contents_validator(self):
        testfile = open(
            path.join(TESTFILES_PATH, 'TrendMiner-screenshots.zip'), 'rb')
        response = self.browser.post('/analyse/', {'data': testfile})
        self.assertFormError(
            response, form='form', field='data',
            errors='Archive contains files that are not in XML format')

    def test_xml_wf_validator(self):
        testzip = open(
            path.join(TESTFILES_PATH, 'archive-with-malformed-xml.zip'), 'rb')
        response = self.browser.post('/analyse/', {'data': testzip})
        self.assertFormError(
            response, form='form', field='data',
            errors=['Archive contains XML files that are not well-formed',
                    'Archive contains XML files that do not validate ' \
                        'against the TrendMiner XML schema'])
        testxml = open(path.join(TESTFILES_PATH, 'malformed.xml'))
        response = self.browser.post('/analyse/', {'data': testxml})
        self.assertFormError(
            response, form='form', field='data',
            errors=['XML file is not well-formed',
                    'XML file does not validate against TrendMiner ' \
                        'XML Schema'])

    def test_xml_schema_validator(self):
        testzip = open(
            path.join(TESTFILES_PATH, 'archive-with-valid-xml.zip'), 'rb')
        response = self.browser.post('/analyse/', {'data': testzip})
        self.assertFormError(
            response, form='form', field='data',
            errors='Archive contains XML files that do not validate ' \
                'against the TrendMiner XML schema')
        testxml = open(path.join(TESTFILES_PATH, 'valid.xml'))
        response = self.browser.post('/analyse/', {'data': testxml})
        self.assertFormError(
            response, form='form', field='data',
            errors='XML file does not validate against TrendMiner ' \
                'XML Schema')
