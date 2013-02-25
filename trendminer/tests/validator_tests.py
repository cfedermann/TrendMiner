import os
import shutil
import tempfile
import zipfile

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from settings import MAX_UPLOAD_SIZE, ROOT_PATH, TESTFILES_PATH
from trendminer import UploadFormErrors
from utils import add_timestamp_prefix, get_file_ext, remove_upload


class ValidatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testdir = tempfile.mkdtemp(suffix='.test', dir=ROOT_PATH)
        cls.file_prefix = add_timestamp_prefix('')
        cls.uploaded_files = []

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.testdir)
        cls.__delete_uploaded_files()

    @classmethod
    def __delete_uploaded_files(self):
        for upload in self.uploaded_files:
            remove_upload(upload)

    def setUp(self):
        self.user = User.objects.create_user(
            username='trendminer-demo', password='trendminer-demo')
        self.browser = Client()
        self.browser.login(
            username=self.user.username, password='trendminer-demo')

    def tearDown(self):
        self.browser.logout()

    def __create_temp_file(self, extension, size):
        temp_file = tempfile.NamedTemporaryFile(
            prefix=self.file_prefix, suffix=extension, dir=self.testdir)
        temp_file.truncate(size)
        return temp_file

    def __create_test_xml(self, name, content):
        xml_file = open(
            os.path.join(self.testdir, name), 'w')
        xml_file.write(content)
        xml_file.close()
        return name

    def __create_test_zip(self, name, *files):
        zip_file = zipfile.ZipFile(
            os.path.join(self.testdir, name), 'w')
        os.chdir(self.testdir)
        for file_name in files:
            zip_file.write(os.path.basename(file_name))
        os.chdir(os.path.dirname(self.testdir))
        zip_file.close()
        return name

    def __open_test_file(self, file_path):
        flag = 'rb' if not get_file_ext(file_path) == '.xml' else 'r'
        return open(file_path, flag)

    def __check_form_errors(self, file_name, expected_errors):
        with self.__open_test_file(file_name) as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data', errors=expected_errors)
        self.uploaded_files.append(os.path.basename(file_name))

    def test_ext_validator(self):
        with self.__create_temp_file('.png', 1024) as temp_file:
            self.__check_form_errors(
                temp_file.name, UploadFormErrors.EXTENSION)

    def test_size_validator(self):
        with self.__create_temp_file('.zip', MAX_UPLOAD_SIZE+1) as temp_file:
            self.__check_form_errors(temp_file.name, UploadFormErrors.SIZE)
        with self.__create_temp_file('.xml', MAX_UPLOAD_SIZE+1) as temp_file:
            self.__check_form_errors(temp_file.name, UploadFormErrors.SIZE)

    def test_mime_type_validator(self):
        with self.__create_temp_file('.zip', 1024) as temp_file:
            self.__check_form_errors(
                temp_file.name, UploadFormErrors.MIME_TYPE.format(
                    '.zip', 'application/octet-stream'))
        with self.__create_temp_file('.xml', 1024) as temp_file:
            self.__check_form_errors(
                temp_file.name, UploadFormErrors.MIME_TYPE.format(
                    '.xml', 'application/octet-stream'))

    def test_zip_integrity_validator(self):
        file_path = os.path.join(
            TESTFILES_PATH, '2013-01-01_12-00-00_corrupt.zip')
        if os.path.exists(file_path):
            self.__check_form_errors(
                file_path, UploadFormErrors.ZIP_INTEGRITY)

    def test_zip_contents_validator(self):
        with self.__create_temp_file('.png', 1024) as temp_file:
            test_zip = self.__create_test_zip(
                self.file_prefix+'png.zip', temp_file.name)
            self.__check_form_errors(
                os.path.join(self.testdir, test_zip),
                UploadFormErrors.ZIP_CONTENTS)

    def test_xml_wf_validator(self):
        test_file = self.__create_test_xml(
            self.file_prefix+'malformed.xml', 'This is not valid XML.')
        self.__check_form_errors(
            os.path.join(self.testdir, test_file),
            UploadFormErrors.XML_WELLFORMEDNESS)
        test_zip = self.__create_test_zip(
            self.file_prefix+'malformed-xml.zip', test_file)
        self.__check_form_errors(
            os.path.join(self.testdir, test_zip),
            UploadFormErrors.FILES_WELLFORMEDNESS)

    def test_xml_schema_validator(self):
        test_file = self.__create_test_xml(
            self.file_prefix+'valid.xml',
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' \
                '<document></document>')
        self.__check_form_errors(
            os.path.join(self.testdir, test_file),
            UploadFormErrors.XML_SCHEMA_CONFORMITY)
        test_zip = self.__create_test_zip(
            self.file_prefix+'valid-xml.zip', test_file)
        self.__check_form_errors(
            os.path.join(self.testdir, test_zip),
            UploadFormErrors.FILES_SCHEMA_CONFORMITY)

    def test_successful_cases(self):
        test_file = self.__create_test_xml(
            self.file_prefix+'schema-conforming.xml',
            '<item>\n' \
                '<identificativo>XY2013010101234</identificativo>\n' \
                '<data>2013-01-01</data>\n' \
                '<sigla>XY</sigla>\n' \
                '<classe>1</classe>\n' \
                '<dimensione>1234</dimensione>\n' \
                '<titolo></titolo>\n' \
                '<TESTATA></TESTATA>\n' \
                '<TITOLO></TITOLO>\n' \
                '<TESTO></TESTO>\n' \
                '<database>DOCTYPE=HTML</database>\n' \
                '</item>')
        with self.__open_test_file(
            os.path.join(self.testdir, test_file)) as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertContains(response, 'Success!')
        self.uploaded_files.append(test_file)
        test_zip = self.__create_test_zip(
            self.file_prefix+'schema-conforming-xml.zip', test_file)
        with self.__open_test_file(
            os.path.join(self.testdir, test_zip)) as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertContains(response, 'Success!')
        self.uploaded_files.append(test_zip)
