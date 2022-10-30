from flask import g
from tests import BaseTestCase, seed_all


class TestWithoutUser(BaseTestCase):

    def setUp(self):
        super().setUp()
        seed_all(self)
        self.client = self.app.test_client()

    def test_routes(self):
        redirect = b'>Please log in to access this page.</div>'
        test_data = [
            {
                'route': '/u/public_user1',
                'code': 200,
                'assert': b'<h3>public_user1</h3>'
            },
            {
                'route': '/u/private_user1',
                'code': 404,
                'assert': b''
            },
            {
                'route': '/u/edit',
                'code': 200,
                'assert': redirect
            },
            {
                'route': '/u/following',
                'code': 200,
                'assert': redirect
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)


class TestWithPublicUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        seed_all(self)
        self.client = self.app.test_client(user=self.public_user1)

    def test_routes(self):
        test_data = [
            {
                'route': '/u/public_user1',
                'code': 200,
                'assert': b'<h3>public_user1</h3>'
            },
            {
                'route': '/u/private_user1',
                'code': 404,
                'assert': b''
            },
            {
                'route': '/u/edit',
                'code': 200,
                'assert': b'for="username">Username</label>'
            },
            {
                'route': '/u/following',
                'code': 200,
                'assert': b'<h1>Followed Projects</h1>'
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_edit(self):
        good_assert = b'<div class="alert alert-info">Profile successfully updated</div>'
        test_data = [
            {'data': {'email': self.public_user2.email,
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Username or email already taken</div>'
             },
            {'data': {'email': '',
                      'username': self.public_user2.username,
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Username or email already taken</div>'
             },
            {'data': {'email': '',
                      'username': '',
                      'password': '123',
                      'confirm': '123',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Field must be between 8 and 32 characters long.'
             },
            {'data': {'email': 'notanemail',
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Invalid email address.'
             },
            {'data': {'email': '',
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': 'newemail@gmail.com',
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': '',
                      'username': 'NewUsername',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': '',
                      'username': '',
                      'password': 'newPassword',
                      'confirm': 'newPassword',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': 'newemail@gmail.com',
                      'username': 'NewUsername',
                               'password': 'newPassword2',
                               'confirm': 'newPassword2',
                               'old_password': 'newPassword'
                      },
             'code': 200,
             'assert': good_assert
             },
        ]

        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/u/edit', test)


class TestWithPrivateUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        seed_all(self)
        self.client = self.app.test_client(user=self.private_user1)

    def test_routes(self):
        test_data = [
            {
                'route': '/u/public_user1',
                'code': 200,
                'assert': b'<h3>public_user1</h3>'
            },
            {
                'route': '/u/private_user1',
                'code': 200,
                'assert': b'<h3>private_user1</h3>'
            },
            {
                'route': '/u/private_user2',
                'code': 404,
                'assert': b''
            },
            {
                'route': '/u/edit',
                'code': 200,
                'assert': b'for="username">Username</label>'
            },
            {
                'route': '/u/following',
                'code': 200,
                'assert': b'<h1>Followed Projects</h1>'
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_edit(self):
        good_assert = b'<div class="alert alert-info">Profile successfully updated</div>'
        test_data = [
            {'data': {'email': self.public_user2.email,
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Username or email already taken</div>'
             },
            {'data': {'email': '',
                      'username': self.public_user2.username,
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Username or email already taken</div>'
             },
            {'data': {'email': '',
                      'username': '',
                      'password': '123',
                      'confirm': '123',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Field must be between 8 and 32 characters long.'
             },
            {'data': {'email': 'notanemail',
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': b'Invalid email address.'
             },
            {'data': {'email': '',
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': 'newemail@gmail.com',
                      'username': '',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': '',
                      'username': 'NewUsername',
                      'password': '',
                      'confirm': '',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': '',
                      'username': '',
                      'password': 'newPassword',
                      'confirm': 'newPassword',
                      'old_password': 'Password'
                      },
             'code': 200,
             'assert': good_assert
             },
            {'data': {'email': 'newemail@gmail.com',
                      'username': 'NewUsername',
                               'password': 'newPassword2',
                               'confirm': 'newPassword2',
                               'old_password': 'newPassword'
                      },
             'code': 200,
             'assert': good_assert
             },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/u/edit', test)
