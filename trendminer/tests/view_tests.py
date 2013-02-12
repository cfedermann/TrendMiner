from django.test import TestCase
from django.test.client import Client

class ViewTest(TestCase):
    def setUp(self):
        self.browser = Client()

    def test_home_view(self):
        response = self.browser.get('/')
        self.assertEquals(response.status_code, 200)

    def test_login_view(self):
        response = self.browser.get('/login/')
        self.assertEquals(response.status_code, 200)

    def test_analyse_view(self):
        response = self.browser.get('/analyse/')
        self.assertRedirects(response, '/login/?next=/analyse/')
