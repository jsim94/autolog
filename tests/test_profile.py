from sqlalchemy.exc import NoResultFound, IntegrityError, DataError

from tests import BaseTestCase, seed_users
from app.models import User


class UserModelTestCase(BaseTestCase):
    ''''''

    def setUp(self):
        super().setUp()
        seed_users(self)

    def test_get_by_username(self):

        test1 = User.get_by_username(self.public_user1.username)
        self.assertIs(test1, self.public_user1)

        with self.assertRaises(NoResultFound):
            test2 = User.get_by_username('user3')

    def test_get_by_id(self):

        test1 = User.get_by_id(self.public_user1.id)
        self.assertIs(test1, self.public_user1)

        with self.assertRaises(NoResultFound):
            test2 = User.get_by_id('NOTANID')

    def test_validate(self):

        # good - passed user
        test1 = User.authenticate(
            user=self.public_user1, password='Password')
        self.assertIs(test1, self.public_user1)

        # good - passed username
        test2 = User.authenticate(
            username=self.public_user1.username, password='Password')
        self.assertIs(test2, self.public_user1)

        # good - passed user_id
        test3 = User.authenticate(
            id=self.public_user1.id, password='Password')
        self.assertIs(test3, self.public_user1)

        # bad username
        with self.assertRaises(NoResultFound):
            test4 = User.authenticate(
                username='test4', password='Password')

        # bad user id
        with self.assertRaises(NoResultFound):
            test5 = User.authenticate(
                id='75DDCDB04FE511EDB71EBB58DF22EDE5', password='Password')

        # bad password
        test3 = User.authenticate(
            id=self.public_user1.id, password='Password123')
        self.assertIs(test3, None)

    def test_signup(self):
        # good - unique signup
        test1 = User.signup(
            username='NewUser', email='NewUser@email.com', password='NewUserPassword')
        self.assertIsInstance(test1, User)

        #  bad - username too long
        with self.assertRaises(DataError):
            test2 = User.signup(
                username='badUserbadUserbadUserbad', email='NewUser@email.com', password='NewUserPassword')
        with self.assertRaises(NoResultFound):
            _test2 = User.get_by_username('badUserbadUserbadUserbad')

        #  bad - username too short
        with self.assertRaises(IntegrityError):
            test3 = User.signup(
                username='usr', email='test3@email.com', password='NewUserPassword')
        with self.assertRaises(NoResultFound):
            _test3 = User.get_by_username('usr')

        # bad - password too short
        with self.assertRaises(AssertionError):
            test4 = User.signup(
                username='test4', email='test4@email.com', password='NewUser')
        with self.assertRaises(NoResultFound):
            _test4 = User.get_by_username('test4')

        # bad - password too long
        with self.assertRaises(AssertionError):
            test5 = User.signup(
                username='test5', email='test5@email.com', password='NewUserPasswordNewUserPasswordNewUserPassword')
        with self.assertRaises(NoResultFound):
            _test5 = User.get_by_username('test5')

        # bad - repeat username
        with self.assertRaises(IntegrityError):
            test6 = User.signup(
                username='public_user1', email='test6@email.com', password='NewUserPassword')
        with self.assertRaises(NoResultFound):
            _test6 = User.get_by_username('test6')

        # bad - repeat email
        with self.assertRaises(IntegrityError):
            test7 = User.signup(
                username='test7', email='public_user1@test.com', password='NewUserPassword')
        with self.assertRaises(NoResultFound):
            _test7 = User.get_by_username('test7')

    def test_edit(self):
        # good - only change username
        test1 = self.public_user1.edit(username='2public_user1')
        self.assertEqual(test1.username, '2public_user1')

        # good - only change email
        test2 = self.public_user1.edit(email='test2@email.com')
        self.assertEqual(test1.email, 'test2@email.com')

        # good - only change password
        password = 'Thisisanewpassword'
        test3 = self.public_user1.edit(password=password)
        _test3 = User.authenticate(password, user=self.public_user1)
        self.assertIs(_test3, self.public_user1)

        # bad - repeat username
        with self.assertRaises(IntegrityError):
            test4 = self.public_user2.edit(username='2public_user1')

        # bad - repeat email
        with self.assertRaises(IntegrityError):
            test5 = self.public_user2.edit(email='test2@email.com')

        # bad - column does not exist in table
        with self.assertRaises(TypeError):
            test6 = self.public_user2.edit(bad_param='TestFail')

    def test_delete(self):
        self.public_user1.delete()
        with self.assertRaises(NoResultFound):
            test1 = User.get_by_username(self.public_user1.username)

        self.public_user2.delete()
        with self.assertRaises(NoResultFound):
            test1 = User.get_by_username(self.public_user2.username)
