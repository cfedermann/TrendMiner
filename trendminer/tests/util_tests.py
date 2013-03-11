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
    """
    This class provides tests for utility functions defined in
    `utils.py`.

    Each function defined in `utils.py` is tested using a single
    method of this class. Test functions are named after the function
    they test. They are prefixed with `test_`. The `setUpClass` method
    sets up the test environment and is called once before any of the
    individual tests are run. The `tearDown` method is responsible for
    cleaning up the test environment and is called after each
    individual test.
    """

    @classmethod
    def setUpClass(cls):
        """
        Specify upload directory, generic file name and file prefix to
        be used by different tests belonging to this class.
        """
        cls.upload_dir = gettempdir()
        cls.file_name = 'test.txt'
        cls.file_prefix = '2013-01-01_12-00-00_'

    def tearDown(self):
        """
        Remove any files and folders created for the purpose of
        testing.

        This method uses the file prefix defined in `setUpClass` to
        detect files in the upload directory that were created for the
        purpose of testing.
        """
        for entry in os.listdir(self.upload_dir):
            if entry.startswith(self.file_prefix):
                path = os.path.join(self.upload_dir, entry)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

    def __create_temp_file(self, extension, size):
        """
        Create a named temporary file with the specified extension and
        size in the upload directory of the test environment and
        return it.
        """
        temp_file = tempfile.NamedTemporaryFile(
            prefix=self.file_prefix, suffix=extension, dir=self.upload_dir)
        temp_file.truncate(size)
        return temp_file

    def __create_test_zip(self, name, *files):
        """
        Create a .zip file in the upload directory of the test
        environment and add all files in `*files` to it.

        This method uses the string passed via the `name` parameter to
        name the .zip file. It expects all files to be added to the
        archive to be located in the upload directory of the test
        environment.
        """
        zip_file = zipfile.ZipFile(
            os.path.join(self.upload_dir, name), 'w')
        os.chdir(self.upload_dir)
        for file_name in files:
            zip_file.write(os.path.basename(file_name))
        os.chdir(os.path.dirname(self.upload_dir))
        zip_file.close()
        return name

    def test_prefix_url(self):
        """
        Check if `prefix_url` function correctly builds URLs,
        irrespective of whether the target URL is affixed with slashes
        or not.

        Edge cases tested by this method include empty strings and
        strings consisting of a single slash.
        """
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
        """
        Check if `sanitize_file_name` function correctly modifies a
        given file name.

        The function is expected to lowercase the file name, remove
        parentheses and square brackets, and replace spaces with
        underscores.
        """
        file_name = sanitize_file_name('Test (a) [b].txt')
        self.assertEquals(file_name, 'test_a_b.txt')

    def test_add_timestamp_prefix(self):
        """
        Check if `add_timestamp_prefix` function prefixes file names
        correctly.

        If a given file name does not include a timestamp prefix of
        the form `YYYY-MM-DD_hh-mm-ss_`, the function is expected to
        generate one and prepend it to the file name. If the file name
        has been prefixed before, the function is expected to return
        the file name as is.
        """
        file_name = add_timestamp_prefix(self.file_name)
        self.assertTrue(re.match(
                '\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_'+self.file_name,
                file_name))
        file_name = add_timestamp_prefix('')
        self.assertTrue(
            re.match('\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_$', file_name))
        file_name = add_timestamp_prefix(file_name)
        self.assertTrue(
            re.match('\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_$', file_name))

    def test_starts_with_timestamp(self):
        """
        Check if `starts_with_timestamp` function correctly detects
        timestamp prefixes in file names.

        The function is expected to return a `re.match` object if a
        given file name starts with a timestamp prefix of the form
        `YYYY-MM-DD_hh-mm-ss_`. If it doesn't, the function is
        expected to return None.
        """
        file_name = self.file_prefix + self.file_name
        self.assertIsNotNone(starts_with_timestamp(file_name))
        self.assertIsNone(starts_with_timestamp(self.file_name))

    def test_get_tmp_path(self):
        """
        Check if `get_tmp_path` function returns correct path for a
        given file name.

        The function is expected to return an absolute path starting
        with the directory specified by the `TMP_PATH` setting in
        `settings.py`.
        """
        file_path = get_tmp_path(self.file_name)
        self.assertTrue(
            os.path.isabs(file_path) and
            file_path.startswith(self.upload_dir))

    def test_get_file_ext(self):
        """
        Check if `get_file_ext` function correctly returns the
        extension part of a given file name.
        """
        self.assertEquals(get_file_ext(self.file_name), '.txt')

    def test_remove_upload(self):
        """
        Check if `remove_upload` function correctly removes a given
        file from the TrendMiner upload directory.

        For .zip archives, the function is expected to also delete the
        folder into which the files contained in the archive were
        extracted. In order to test it, this method creates a .zip
        file and a folder with the same contents, and checks if both
        of these are removed when calling `remove_upload` on the .zip
        archive.
        """
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
        """
        Check if `store_upload` function correctly stores an uploaded
        file in a given directory.

        The function expects an object of type
        `django.core.files.File` or
        `django.core.files.uploadedfile.UploadedFile`, so in order to
        test it, this method first creates a temporary file,
        constructs an object of type `File` from it and then runs
        store_upload on the latter.
        """
        with self.__create_temp_file('.txt', 1024) as temp_file:
            fake_upload = File(temp_file)
            file_path = os.path.join(self.upload_dir, temp_file.name)
            store_upload(fake_upload, file_path)
            self.assertTrue(os.path.exists(file_path))

    def test_extract_archive(self):
        """
        Check if `extract_archive` function correctly extracts a given
        .zip archive.

        The function is expected to extract the contents of the
        archive to a single folder located in the same directory as
        the archive. The name of the folder is expected to be
        identical to that of the archive without the `.zip` extension.

        To test the function, this method creates a temporary file of
        size 1KB, adds it to a .zip archive, and then runs the
        function on the archive.
        """
        with self.__create_temp_file('.txt', 1024) as temp_file:
            test_zip = self.__create_test_zip(
                self.file_prefix+'.zip', temp_file.name)
            folder = extract_archive(os.path.join(self.upload_dir, test_zip))
            self.assertTrue(os.path.exists(folder))
            self.assertEquals(
                folder, os.path.join(self.upload_dir, self.file_prefix))
