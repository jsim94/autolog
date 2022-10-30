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
                'route': '/',
                'code': 200,
                'assert': b'<h1>Modlog</h1>'
            },
            {
                'route': '/login',
                'code': 200,
                'assert': b'mb-2" id="username" name="username" required'
            },
            {
                'route': '/signup',
                'code': 200,
                'assert': b'>Username</label>'
            },
            {
                'route': '/logout',
                'code': 200,
                'assert': redirect
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_login(self):
        test_data = [
            {
                'data': {
                    'username': self.public_user2.username,
                    'password': 'BadPassword'
                },
                'code': 200,
                'assert': b'alert-danger">Invalid username or password</div>'
            },
            {
                'data': {
                    'username': 'NotAValidUsername',
                    'password': 'Password'
                },
                'code': 200,
                'assert': b'alert-danger">Invalid username or password</div>'
            },
            {
                'data': {
                    'username': self.public_user2.username,
                    'password': 'Password'
                },
                'code': 200,
                'assert': b'<h3>public_user2</h3>'
            }
        ]

        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/login', test)

    def test_signup(self):
        test_data = [
            {
                'data': {
                    'email': 'notanemail',
                    'username': 'NewUser1',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': b'text-danger">Invalid email address.</span>'
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'a',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': b'text-danger">Field must be between'
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'dlawjhkdlwadjakhdjklawhd',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': b'text-danger">Field must be between'
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': '1',
                    'confirm': '1'
                },
                'code': 200,
                'assert': b'text-danger">Field must be between'
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': '179162378912637123123123261381123123927137',
                    'confirm': '179162378912637123123123261381123123927137'
                },
                'code': 200,
                'assert': b'text-danger">Field must be between'
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': 'GoodPassword',
                    'confirm': 'BadPassword'
                },
                'code': 200,
                'assert': b'danger">Passwords must match</span>'
            },
            {
                'data': {
                    'email': self.public_user1.email,
                    'username': 'GoodUsername',
                    'password': 'GoodPassword',
                    'confirm': 'GoodPassword'
                },
                'code': 200,
                'assert': b'alert-danger">Username or email already taken</div>'
            },
            {
                'data': {
                    'email': 'goodemail@gmail.com',
                    'username': self.public_user1.username,
                    'password': 'GoodPassword',
                    'confirm': 'GoodPassword'
                },
                'code': 200,
                'assert': b'alert-danger">Username or email already taken</div>'
            },
            {
                'data': {
                    'email': 'goodemail@gmail.com',
                    'username': 'NewUsername',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': b'<h3>NewUsername</h3>'
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/signup', test)


class TestWithPublicUser(BaseTestCase):

    def setUp(self):
        super().setUp()
        seed_all(self)
        self.client = self.app.test_client(user=self.public_user1)

    def test_routes(self):
        user_home = b'<h3>public_user1</h3>'
        test_data = [
            {
                'route': '/',
                'code': 200,
                'assert': user_home
            },
            {
                'route': '/login',
                'code': 200,
                'assert': user_home
            },
            {
                'route': '/signup',
                'code': 200,
                'assert': user_home
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_login(self):
        redirect = b'<h3>public_user1</h3>'
        test_data = [
            {
                'data': {
                    'username': self.public_user2.username,
                    'password': 'BadPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'username': 'NotAValidUsername',
                    'password': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'username': self.public_user2.username,
                    'password': 'Password'
                },
                'code': 200,
                'assert': redirect
            }
        ]

        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/login', test)

    def test_signup(self):
        redirect = b'<h3>public_user1</h3>'
        test_data = [
            {
                'data': {
                    'email': 'notanemail',
                    'username': 'NewUser1',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'a',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'dlawjhkdlwadjakhdjklawhd',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': '1',
                    'confirm': '1'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': '179162378912637123123123261381123123927137',
                    'confirm': '179162378912637123123123261381123123927137'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': 'GoodPassword',
                    'confirm': 'BadPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': self.public_user1.email,
                    'username': 'GoodUsername',
                    'password': 'GoodPassword',
                    'confirm': 'GoodPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@gmail.com',
                    'username': self.public_user1.username,
                    'password': 'GoodPassword',
                    'confirm': 'GoodPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@gmail.com',
                    'username': 'NewUsername',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/signup', test)

    def test_logout(self):
        with self.client as client:
            resp = client.get('/logout', follow_redirects=True)

            self.assertIs(getattr(g, 'current_user', None), None)


class TestWithPrivateUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        seed_all(self)
        self.client = self.app.test_client(user=self.private_user1)

    def test_routes(self):
        user_home = b'<h3>private_user1</h3>'
        test_data = [
            {
                'route': '/',
                'code': 200,
                'assert': user_home
            },
            {
                'route': '/login',
                'code': 200,
                'assert': user_home
            },
            {
                'route': '/signup',
                'code': 200,
                'assert': user_home
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_login(self):
        redirect = b'<h3>private_user1</h3>'
        test_data = [
            {
                'data': {
                    'username': self.public_user1.username,
                    'password': 'BadPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'username': 'NotAValidUsername',
                    'password': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'username': self.public_user2.username,
                    'password': 'Password'
                },
                'code': 200,
                'assert': redirect
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/login', test)

    def test_signup(self):
        redirect = b'<h3>private_user1</h3>'
        test_data = [
            {
                'data': {
                    'email': 'notanemail',
                    'username': 'NewUser1',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'a',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'dlawjhkdlwadjakhdjklawhd',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': '1',
                    'confirm': '1'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': '179162378912637123123123261381123123927137',
                    'confirm': '179162378912637123123123261381123123927137'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@aol.com',
                    'username': 'GoodUsername',
                    'password': 'GoodPassword',
                    'confirm': 'BadPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': self.private_user1.email,
                    'username': 'GoodUsername',
                    'password': 'GoodPassword',
                    'confirm': 'GoodPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@gmail.com',
                    'username': self.private_user1.username,
                    'password': 'GoodPassword',
                    'confirm': 'GoodPassword'
                },
                'code': 200,
                'assert': redirect
            },
            {
                'data': {
                    'email': 'goodemail@gmail.com',
                    'username': 'NewUsername',
                    'password': 'Password',
                    'confirm': 'Password'
                },
                'code': 200,
                'assert': redirect
            },
        ]

        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/signup', test)

    def test_logout(self):
        with self.client as client:
            resp = client.get('/logout', follow_redirects=True)

            self.assertIs(getattr(g, 'current_user', None), None)
