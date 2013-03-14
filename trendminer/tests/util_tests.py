"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""

import os
import re
import shutil
import tempfile
import zipfile

from tempfile import gettempdir
from django.core.files import File
from django.test import TestCase

from settings import URL_PREFIX
from utils import add_timestamp_prefix, extract_archive
from utils import get_file_ext, get_tmp_path, prefix_url, remove_upload
from utils import sanitize_file_name, starts_with_timestamp, store_upload


class UtilTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upload_dir = gettempdir()
        cls.file_name = 'test.txt'
        cls.file_prefix = '2013-01-01_12-00-00_'

    def tearDown(self):
        for entry in os.listdir(self.upload_dir):
            if entry.startswith(self.file_prefix):
                path = os.path.join(self.upload_dir, entry)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

    def __create_temp_file(self, extension, size):
        temp_file = tempfile.NamedTemporaryFile(
            prefix=self.file_prefix, suffix=extension, dir=self.upload_dir)
        temp_file.truncate(size)
        return temp_file

    def __create_test_zip(self, name, *files):
        zip_file = zipfile.ZipFile(
            os.path.join(self.upload_dir, name), 'w')
        os.chdir(self.upload_dir)
        for file_name in files:
            zip_file.write(os.path.basename(file_name))
        os.chdir(os.path.dirname(self.upload_dir))
        zip_file.close()
        return name

    def test_prefix_url(self):
        bare_prefix = URL_PREFIX.strip('/')
        url = prefix_url('')
        self.assertEquals(url, '/{}/'.format(bare_prefix))
        url = prefix_url('/')
        self.assertEquals(url, '/{}/'.format(bare_prefix))
        url = prefix_url('foo')
        self.assertEquals(url, '/{}/foo/'.format(bare_prefix))
        url = prefix_url('/foo')
        self.assertEquals(url, '/{}/foo/'.format(bare_prefix))
        url = prefix_url('foo/')
        self.assertEquals(url, '/{}/foo/'.format(bare_prefix))
        url = prefix_url('/foo/')
        self.assertEquals(url, '/{}/foo/'.format(bare_prefix))

    def test_sanitize_file_name(self):
        file_name = sanitize_file_name('Test (a) [b].txt')
        self.assertEquals(file_name, 'test_a_b.txt')

    def test_add_timestamp_prefix(self):
        file_name = add_timestamp_prefix(self.file_name)
        self.assertTrue(
            re.match('\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_', file_name))
        file_name = add_timestamp_prefix('')
        self.assertTrue(
            re.match('\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_$', file_name))

    def test_starts_with_timestamp(self):
        file_name = self.file_prefix + self.file_name
        self.assertIsNotNone(starts_with_timestamp(file_name))

    def test_get_tmp_path(self):
        file_path = get_tmp_path(self.file_name)
        self.assertTrue(file_path.startswith(self.upload_dir))

    def test_get_file_ext(self):
        self.assertEquals(get_file_ext(self.file_name), '.txt')

    def test_remove_upload(self):
        with self.__create_temp_file('.txt', 1024) as temp_file:
            test_zip = self.__create_test_zip(
                self.file_prefix+'.zip', temp_file.name)
            folder = os.path.join(self.upload_dir, self.file_prefix)
            os.mkdir(folder)
            shutil.copyfile(temp_file.name, os.path.join(
                    folder, os.path.basename(temp_file.name)))
            remove_upload(test_zip)
            self.assertFalse(
                os.path.exists(os.path.join(self.upload_dir, test_zip)))
            self.assertFalse(os.path.exists(folder))

    def test_store_upload(self):
        with self.__create_temp_file('.txt', 1024) as temp_file:
            fake_upload = File(temp_file)
            file_path = os.path.join(self.upload_dir, temp_file.name)
            store_upload(fake_upload, file_path)
            self.assertTrue(os.path.exists(file_path))

    def test_extract_archive(self):
        with self.__create_temp_file('.txt', 1024) as temp_file:
            test_zip = self.__create_test_zip(
                self.file_prefix+'.zip', temp_file.name)
            folder = extract_archive(os.path.join(self.upload_dir, test_zip))
            self.assertTrue(os.path.exists(folder))
