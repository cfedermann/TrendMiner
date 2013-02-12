from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

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
        pass

    def test_size_validator(self):
        pass

    def test_mime_type_validator(self):
        pass

    def test_zip_integrity_validator(self):
        pass

    def test_zip_contents_validator(self):
        pass

    def test_xml_wf_validator(self):
        pass

    def test_xml_schema_validator(self):
        pass
