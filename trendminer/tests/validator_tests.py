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

    def __check_form_errors(self, file_name, expected_errors):
        with get_test_file(file_name) as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data', errors=expected_errors)

    def test_ext_validator(self):
        self.__check_form_errors(
            'trendminer-logo-final.png', UploadFormErrors.EXTENSION)

    def test_size_validator(self):
        self.__check_form_errors('large.zip', UploadFormErrors.SIZE)
        self.__check_form_errors('large.xml', UploadFormErrors.SIZE)

    def test_mime_type_validator(self):
        self.__check_form_errors(
            'fake.zip', UploadFormErrors.MIME_TYPE.format(
                '.zip', 'text/plain'))
        self.__check_form_errors(
            'fake.xml', UploadFormErrors.MIME_TYPE.format(
                '.xml', 'application/zip'))

    def test_zip_integrity_validator(self):
        self.__check_form_errors(
            'corrupt.zip', UploadFormErrors.ZIP_INTEGRITY)

    def test_zip_contents_validator(self):
        self.__check_form_errors(
            'TrendMiner-screenshots.zip', UploadFormErrors.ZIP_CONTENTS)

    def test_xml_wf_validator(self):
        self.__check_form_errors(
            'archive-with-malformed-xml.zip',
            UploadFormErrors.FILES_WELLFORMEDNESS)
        self.__check_form_errors(
            'malformed.xml', UploadFormErrors.XML_WELLFORMEDNESS)

    def test_xml_schema_validator(self):
        self.__check_form_errors(
            'archive-with-valid-xml.zip',
            UploadFormErrors.FILES_SCHEMA_CONFORMITY)
        self.__check_form_errors(
            'valid.xml', UploadFormErrors.XML_SCHEMA_CONFORMITY)

    def test_successful_cases(self):
        with get_test_file('reputation_test3.zip') as testzip:
            response = self.browser.post('/analyse/', {'data': testzip})
            self.assertContains(response, 'Success!')
        with get_test_file('RR2009042290839-only-quant.xml') as testxml:
            response = self.browser.post('/analyse/', {'data': testxml})
            self.assertContains(response, 'Success!')
