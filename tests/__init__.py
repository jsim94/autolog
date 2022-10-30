import os
import unittest
from flask_login import FlaskLoginClient

from app import create_app
from app import models
from .seed import *


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['FLASK_CONFIG'] = 'config.TestConfig'
        cls.app = create_app()

    def setUp(self):
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.app.test_client_class = FlaskLoginClient

        with self.app_ctx:
            models.db.drop_all()
            models.db.create_all()

    def tearDown(self):
        models.db.session.remove()

    def check_get_request(self, client, route, test):
        resp = client.get(
            route,
            follow_redirects=True
        )
        try:
            self.assertEqual(test['code'], resp.status_code)
            self.assertIn(
                test['assert'], resp.data)
        except:
            print(f'Bad test: {test}')
            raise
        print('passed...')

    def check_post_request(self, client, route, test):
        resp = client.post(
            route,
            data=test['data'],
            follow_redirects=True
        )
        try:
            self.assertEqual(test['code'], resp.status_code)
            self.assertIn(
                test['assert'], resp.data)
        except:
            print(f'Bad test: {test}')
            raise
        print('passed...')


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
