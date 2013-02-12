from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from trendminer import UploadFormErrors
from utils import get_test_file


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
        with get_test_file('trendminer-logo-final.png') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.EXTENSION)

    def test_size_validator(self):
        with get_test_file('large.zip') as testzip:
            response = self.browser.post('/analyse/', {'data': testzip})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.SIZE)
        with get_test_file('large.xml') as testxml:
            response = self.browser.post('/analyse/', {'data': testxml})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.SIZE)

    def test_mime_type_validator(self):
        with get_test_file('fake.zip') as testzip:
            response = self.browser.post('/analyse/', {'data': testzip})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.MIME_TYPE.format(
                    '.zip', 'text/plain'))
        with get_test_file('fake.xml') as testxml:
            response = self.browser.post('/analyse/', {'data': testxml})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.MIME_TYPE.format(
                    '.xml', 'application/zip'))

    def test_zip_integrity_validator(self):
        with get_test_file('corrupt.zip') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.ZIP_INTEGRITY)

    def test_zip_contents_validator(self):
        with get_test_file('TrendMiner-screenshots.zip') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.ZIP_CONTENTS)

    def test_xml_wf_validator(self):
        with get_test_file('archive-with-malformed-xml.zip') as testzip:
            response = self.browser.post('/analyse/', {'data': testzip})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.FILES_WELLFORMEDNESS)
        with get_test_file('malformed.xml') as testxml:
            response = self.browser.post('/analyse/', {'data': testxml})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.XML_WELLFORMEDNESS)

    def test_xml_schema_validator(self):
        with get_test_file('archive-with-valid-xml.zip') as testzip:
            response = self.browser.post('/analyse/', {'data': testzip})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.FILES_SCHEMA_CONFORMITY)
        with get_test_file('valid.xml') as testxml:
            response = self.browser.post('/analyse/', {'data': testxml})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.XML_SCHEMA_CONFORMITY)
