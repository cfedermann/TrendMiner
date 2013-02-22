import os
import shutil
import tempfile
import zipfile

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from settings import MAX_UPLOAD_SIZE, ROOT_PATH
from trendminer import UploadFormErrors
from utils import create_unique_file_name, get_test_file, get_tmp_path


class ValidatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testdir = tempfile.mkdtemp(suffix='.test', dir=ROOT_PATH)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.testdir)

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
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', dir=self.testdir)
        temp_file.truncate(1024)
        with open(temp_file.name, 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.EXTENSION)
        temp_file.close()

    def test_size_validator(self):
        prefix = create_unique_file_name('')
        temp_file = tempfile.NamedTemporaryFile(
            prefix=prefix, suffix='.zip', dir=self.testdir)
        temp_file.truncate(MAX_UPLOAD_SIZE+1)
        with open(temp_file.name, 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.SIZE)
        temp_file.close()
        os.remove(get_tmp_path(os.path.basename(temp_file.name.lower())))

        temp_file = tempfile.NamedTemporaryFile(
            prefix=prefix, suffix='.xml', dir=self.testdir)
        temp_file.truncate(MAX_UPLOAD_SIZE+1)
        with open(temp_file.name, 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.SIZE)
        temp_file.close()
        os.remove(get_tmp_path(os.path.basename(temp_file.name.lower())))

    def test_mime_type_validator(self):
        prefix = create_unique_file_name('fake')
        temp_file = tempfile.NamedTemporaryFile(
            prefix=prefix, suffix='.zip', dir=self.testdir)
        temp_file.truncate(1024)
        with open(temp_file.name, 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.MIME_TYPE.format(
                    '.zip', 'application/octet-stream'))
        temp_file.close()
        os.remove(get_tmp_path(os.path.basename(temp_file.name.lower())))
        temp_file = tempfile.NamedTemporaryFile(
            prefix=prefix, suffix='.xml', dir=self.testdir)
        temp_file.truncate(1024)
        with open(temp_file.name, 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.MIME_TYPE.format(
                    '.xml', 'application/octet-stream'))
        temp_file.close()
        os.remove(get_tmp_path(os.path.basename(temp_file.name.lower())))

    def test_zip_integrity_validator(self):
        self.__check_form_errors(
            '2013-01-01_12-00-00_corrupt.zip',
            UploadFormErrors.ZIP_INTEGRITY)
        os.remove(get_tmp_path('2013-01-01_12-00-00_corrupt.zip'))

    def test_zip_contents_validator(self):
        prefix = create_unique_file_name('')
        temp_file = tempfile.NamedTemporaryFile(
            prefix=prefix, suffix='.txt', dir=self.testdir)
        temp_file.truncate(1024)
        temp_zip = zipfile.ZipFile(
            os.path.join(self.testdir, prefix+'txt.zip'), 'w')
        os.chdir(self.testdir)
        temp_zip.write(os.path.basename(temp_file.name))
        os.chdir(os.path.dirname(self.testdir))
        temp_zip.close()
        with open(os.path.join(
                self.testdir, prefix+'txt.zip'), 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.ZIP_CONTENTS)
        temp_file.close()
        os.remove(get_tmp_path(prefix+'txt.zip'))
        shutil.rmtree(get_tmp_path(prefix+'txt'))

    def test_xml_wf_validator(self):
        prefix = create_unique_file_name('')
        temp_file = open(
            os.path.join(self.testdir, prefix+'malformed.xml'), 'w')
        temp_file.write('This is not valid XML.')
        temp_file.close()
        with open(os.path.join(
                self.testdir, prefix+'malformed.xml'), 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.XML_WELLFORMEDNESS)
        os.remove(get_tmp_path(prefix+'malformed.xml'))
        temp_zip = zipfile.ZipFile(
            os.path.join(self.testdir, prefix+'malformed-xml.zip'), 'w')
        os.chdir(self.testdir)
        temp_zip.write(prefix+'malformed.xml')
        os.chdir(os.path.dirname(self.testdir))
        temp_zip.close()
        with open(os.path.join(
                self.testdir, prefix+'malformed-xml.zip'), 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.FILES_WELLFORMEDNESS)
        os.remove(get_tmp_path(prefix+'malformed-xml.zip'))
        shutil.rmtree(get_tmp_path(prefix+'malformed-xml'))

    def test_xml_schema_validator(self):
        prefix = create_unique_file_name('')
        temp_file = open(
            os.path.join(self.testdir, prefix+'valid.xml'), 'w')
        temp_file.write(
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' \
                '<document></document>')
        temp_file.close()
        with open(os.path.join(
                self.testdir, prefix+'valid.xml'), 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.XML_SCHEMA_CONFORMITY)
        os.remove(get_tmp_path(prefix+'valid.xml'))
        temp_zip = zipfile.ZipFile(
            os.path.join(self.testdir, prefix+'valid-xml.zip'), 'w')
        os.chdir(self.testdir)
        temp_zip.write(prefix+'valid.xml')
        os.chdir(os.path.dirname(self.testdir))
        temp_zip.close()
        with open(os.path.join(
                self.testdir, prefix+'valid-xml.zip'), 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertFormError(
                response, form='form', field='data',
                errors=UploadFormErrors.FILES_SCHEMA_CONFORMITY)
        os.remove(get_tmp_path(prefix+'valid-xml.zip'))
        shutil.rmtree(get_tmp_path(prefix+'valid-xml'))

    def test_successful_cases(self):
        prefix = create_unique_file_name('')
        temp_file = open(
            os.path.join(self.testdir, prefix+'schema-conforming.xml'), 'w')
        temp_file.write(
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
        temp_file.close()
        with open(os.path.join(
                self.testdir,
                prefix+'schema-conforming.xml'), 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertContains(response, 'Success!')
        os.remove(get_tmp_path(prefix+'schema-conforming.xml'))
        temp_zip = zipfile.ZipFile(
            os.path.join(
                self.testdir, prefix+'schema-conforming-xml.zip'), 'w')
        os.chdir(self.testdir)
        temp_zip.write(prefix+'schema-conforming.xml')
        os.chdir(os.path.dirname(self.testdir))
        temp_zip.close()
        with open(os.path.join(
                self.testdir,
                prefix+'schema-conforming-xml.zip'), 'r') as testfile:
            response = self.browser.post('/analyse/', {'data': testfile})
            self.assertContains(response, 'Success!')
        os.remove(get_tmp_path(prefix+'schema-conforming-xml.zip'))
        shutil.rmtree(get_tmp_path(prefix+'schema-conforming-xml'))
