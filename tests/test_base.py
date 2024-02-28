from flask_testing import TestCase
from flask import current_app, url_for

from main import app

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_is_testing(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        from urllib.parse import urlparse
        response = self.client.get(url_for('index'))
        parsed_location = urlparse(response.location)
        self.assertEqual(parsed_location.path, url_for('hello'))

    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assertEqual(response.status_code, 200)

    def test_hello_post(self):
        from urllib.parse import urlparse
        fake_form = {
            'username': 'John',
            'password': 'fake-password'
        }
        response = self.client.post(url_for('hello'), data=fake_form)
        parsed_location = urlparse(response.location)
        self.assertEqual(parsed_location.path, url_for('index'))