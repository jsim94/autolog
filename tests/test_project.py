from sqlalchemy.exc import NoResultFound, IntegrityError, DataError

from tests import BaseTestCase, seed_users, seed_projects
from app.models import Project, Update, Comment


class ProjectModelTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        seed_users(self)
        seed_projects(self)

    def test_get_by_name(self):

        test1 = Project.get_by_name(self.public_project1.name)
        self.assertIs(test1, self.public_project1)

        test2 = Project.get_by_name(self.public_project2.name)
        self.assertIs(test2, self.public_project2)

        with self.assertRaises(NoResultFound):
            test3 = Project.get_by_name('projectNone')

    def test_get_by_id(self):

        test1 = Project.get_by_id(self.public_project1.id)
        self.assertIs(test1, self.public_project1)

        test2 = Project.get_by_id(self.public_project2.id)
        self.assertIs(test2, self.public_project2)

        with self.assertRaises(NoResultFound):
            test3 = Project.get_by_id('NOTANID')

    def test_w2p(self):
        test = self.public_project1.w2p
        self.assertEqual(test, 7.8)

    def test_add_mod(self):
        # good
        self.public_project1.add_mod('Mod1')
        self.assertIn('Mod1', self.public_project1.mods)

        # bad - too long
        with self.assertRaises(AssertionError):
            self.public_project1.add_mod(
                'Extra Long Mod!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        # bad - too short
        with self.assertRaises(AssertionError):
            self.public_project1.add_mod(
                '')

    def test_delete_mod(self):
        # good
        self.public_project2.delete_mod(0)
        self.assertNotIn('Mod1', self.public_project2.mods)

        # bad - wrong index
        with self.assertRaises(IndexError):
            self.public_project2.delete_mod(10)

    def test_add_follow(self):
        # good
        self.public_project2.add_follow(self.public_user1)
        self.assertIn(self.public_user1, self.public_project2.followers)

    def test_remove_follow(self):
        # good
        self.public_project2.add_follow(self.public_user1)
        self.assertIn(self.public_user1, self.public_project2.followers)
        self.public_project2.remove_follow(self.public_user1)
        self.assertNotIn(self.public_user1, self.public_project2.followers)

        # bad - user not following
        with self.assertRaises(ValueError):
            self.public_project2.remove_follow(self.public_user1)

    def test_edit(self):
        # good - change name, description
        self.public_project1.edit(name='2project1',
                                  description="This is a brand new description for project1")
        self.assertEqual(self.public_project1.name, '2project1')
        self.assertEqual(self.public_project1.description,
                         'This is a brand new description for project1')

        # good - change engine size and drivetrain
        self.public_project1.edit(engine_size=6.2, drivetrain='AWD')
        self.assertEqual(self.public_project1.engine_size, 6.2)
        self.assertEqual(self.public_project1.drivetrain.value, 'AWD')

        # bad - description too long
        with self.assertRaises(DataError):
            self.public_project2.edit(description='Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus')

        # # bad - no title
        # with self.assertRaises(IntegrityError):
        self.public_project2.edit(name='')
        self.assertEqual(self.public_project2.name, 'PublicProject2')

        # bad - column does not exist in table
        with self.assertRaises(AttributeError):
            self.public_project2.edit(bad_param='TestFail')

    def test_delete(self):
        self.public_project1.delete()
        with self.assertRaises(NoResultFound):
            test1 = Project.get_by_name(self.public_project1.name)

        self.public_project2.delete()
        with self.assertRaises(NoResultFound):
            test1 = Project.get_by_id(self.public_project2.id)


class UpdateModelTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        seed_users(self)
        seed_projects(self)

    def test_create(self):
        update = Update.create(project_id=self.public_project1.id,
                               title='', content='This is an update')
        self.assertIn(update, self.public_project1.updates)

    def test_edit(self):
        # good
        self.public_project1_update.edit(title='New Title')
        self.assertEqual(self.public_project1_update.title, 'New Title')

        # bad - title too long
        with self.assertRaises(DataError):
            self.public_project1_update.edit(
                title='This Title is Too LongThis Title is Too LongThis Title is Too LongThis Title is Too Long')

        # good - change content
        self.public_project1_update.edit(
            content='This is a new piece of content')
        self.assertEqual(self.public_project1_update.content,
                         'This is a new piece of content')

        # bad - content too long
        with self.assertRaises(DataError):
            self.public_project1_update.edit(content='Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. VivamusLorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cra')

    def test_delete(self):
        update = Update.create(project_id=self.public_project1.id,
                               title='', content='This is an update')
        update.delete()
        self.assertNotIn(update, self.public_project1.updates)


class CommentModelTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        seed_users(self)
        seed_projects(self)

    def test_create(self):
        test1 = Comment.create(project_id=self.public_project1.id,
                               user_id=self.public_user2.id,
                               content='This is a second comment')
        self.assertIn(test1, self.public_project1.comments)
        self.assertIs(test1.user, self.public_user2)

    def test_edit(self):
        # good - change content
        comment = Comment.create(project_id=self.public_project1.id,
                                 user_id=self.public_user2.id,
                                 content='This is a second comment')

        comment.edit(content='This is a new piece of content')
        self.assertEqual(comment.content,
                         'This is a new piece of content')

        # bad - no content
        comment.edit(content='')
        self.assertEqual(comment.content, 'This is a new piece of content')

        # bad - content too long
        with self.assertRaises(DataError):
            comment.edit(content='Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede.')

    def test_delete(self):
        comment = Comment.create(project_id=self.public_project1.id,
                                 user_id=self.public_user2.id,
                                 content='This is a second comment')
        comment.delete()
        self.assertNotIn(comment, self.public_project1.comments)
