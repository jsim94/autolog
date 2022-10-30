from flask import g
from tests import BaseTestCase, seed_all


class TestWithoutUser(BaseTestCase):

    def setUp(self):
        super().setUp()
        seed_all(self)
        self.client = self.app.test_client()

    def test_routes(self):
        redirect = b'alert-message">Please log in to access this page.</div>'
        test_data = [
            {
                'route': '/p/new',
                'code': 200,
                'assert': redirect,
            }, {
                'route': f'/p/{self.public_project1.id}',
                'code': 200,
                'assert': b'<h1 class="d-inline">PublicProject1</h1>',
            }, {
                'route': f'/p/{self.public_project1.id}/edit',
                'code': 403,
                'assert': b'',
            }, {
                'route': f'/p/{self.public_project1.id}/add-follow',
                'code': 200,
                'assert': redirect,
            }, {
                'route': f'/p/{self.public_project1.id}/remove-follow',
                'code': 200,
                'assert': redirect,
            }, {
                'route': f'/p/{self.private_project1.id}',
                'code': 403,
                'assert': b'',
            }, {
                'route': f'/p/{self.private_project1.id}/edit',
                'code': 403,
                'assert': b'',
            }, {
                'route': f'/p/{self.private_project1.id}/add-follow',
                'code': 403,
                'assert': b'',
            }, {
                'route': f'/p/{self.private_project1.id}/remove-follow',
                'code': 403,
                'assert': b'',
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_new(self):
        test_data = [
            {
                'data': {
                    'year': 2007,
                    'make': 'Ford',
                    'model': 'GT500',
                    'model_id': 15175,
                    'name': 'Shelby2',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3900,
                    'drivetrain': 'RWD',
                    'engine_size': 5.4
                },
                'code': 200,
                'assert': b'alert-message">Please log in to access this page.</div>'
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/p/new', test)

    def test_edit(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit',
                'data': {
                    'year': 2007,
                    'make': 'Ford',
                    'model': 'GT500',
                    'model_id': 15175,
                    'name': 'Shelby2',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3900,
                    'drivetrain': 'RWD',
                    'engine_size': 5.4
                },
                'code': 403,
                'assert': b''
            }, {
                'route': f'/p/{self.private_project1.id}/edit',
                'data': {
                    'year': 2007,
                    'make': 'Ford',
                    'model': 'GT500',
                    'model_id': 15175,
                    'name': 'Shelby2',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3900,
                    'drivetrain': 'RWD',
                    'engine_size': 5.4
                },
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete(self):
        with self.client as client:
            resp = client.get(f'/p/{self.public_project1.id}/delete')
            self.assertEqual(resp.status_code, 403)
            self.assertIn(self.public_project1, self.public_user1.projects)

            resp = client.get(f'/p/{self.private_project1.id}/delete')
            self.assertEqual(resp.status_code, 403)
            self.assertIn(self.private_project1, self.private_user1.projects)

    def test_add_mod(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete_mod(self):
        with self.client as client:
            resp = client.delete(f'/p/{self.public_project1.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 403)
            self.assertIn('This is mod1', self.public_project1.mods)

            resp = client.delete(f'/p/{self.private_project1.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 403)
            self.assertIn('This is mod1', self.private_project1.mods)

    def test_new_update(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_edit_update(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit-update/{self.public_project1.updates[0].id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/edit-update/{self.private_project1.updates[0].id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete_update(self):
        with self.client as client:
            resp = client.get(
                f'/p/{self.public_project1.id}/delete-update/{self.public_project1.updates[0]}')
            self.assertIn('This is mod1', self.public_project1.mods)

            resp = client.get(
                f'/p/{self.private_project1.id}/delete-update/{self.private_project1.updates[0]}')
            self.assertIn('This is mod1', self.public_project1.mods)

    def test_new_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/new-comment',
                'data': {'content': 'Test comment'},
                'code': 200,
                'assert': b'alert-message">Please log in to access this page.</div>'
            },
            {
                'route': f'/p/{self.private_project1.id}/new-comment',
                'data': {'content': 'Test comment'},
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_edit_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit-comment/{self.public_project1.comments[0].id}',
                'data': {'content': 'Edited comment'},
                'code': 200,
                'assert': b'alert-message">Please log in to access this page.</div>'
            },
            {
                'route': f'/p/{self.private_project1.id}/edit-comment/{self.private_project1.comments[0].id}',
                'data': {'content': 'Edited comment'},
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/delete-comment/{self.public_project1.comments[0].id}',
                'code': 200,
                'assert': b'alert-message">Please log in to access this page.</div>'
            },
            {
                'route': f'/p/{self.private_project1.id}/delete-comment/{self.private_project1.comments[0].id}',
                'code': 403,
                'assert': b''
            },
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
                'route': '/p/new',
                'code': 200,
                'assert': b'<h1>New Project</h1>'
            },
            # own project
            {
                'route': f'/p/{self.public_project1.id}',
                'code': 200,
                'assert': b'<h1 class="d-inline">PublicProject1</h1>'
            },
            {
                'route': f'/p/{self.public_project1.id}/edit',
                'code': 200,
                'assert': b'<h1>Edit Project</h1>'},
            # public project
            {
                'route': f'/p/{self.public_project2.id}',
                'code': 200,
                'assert': b'<h1 class="d-inline">PublicProject2</h1>'
            },
            {
                'route': f'/p/{self.public_project2.id}/edit',
                'code': 403,
                'assert': b''
            },
            # private project
            {
                'route': f'/p/{self.private_project1.id}',
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/edit',
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_new(self):
        test_data = [
            {
                'data': {
                    'year': 2007,
                    'make': 'Ford',
                    'model': 'GT500',
                    'model_id': 15175,
                    'name': 'Shelby2',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3900,
                    'drivetrain': 'RWD',
                    'engine_size': 5.4
                },
                'code': 200,
                'assert': b'<h1 class="d-inline">Shelby2</h1>'
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/p/new', test)

    def test_edit(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit',
                'data': {
                    'year': 2017,
                    'make': 'Ford',
                    'model': 'Mustang',
                    'model_id': 69569,
                    'name': 'Mustang',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3700,
                    'drivetrain': 'RWD',
                    'engine_size': 5.0
                },
                'code': 200,
                'assert': b'alert-info">Project Successfully edited</div>'
            }, {
                'route': f'/p/{self.public_project2.id}/edit',
                'data': {
                    'year': 2017,
                    'make': 'Ford',
                    'model': 'Mustang',
                    'model_id': 69569,
                    'name': 'Mustang',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3700,
                    'drivetrain': 'RWD',
                    'engine_size': 5.0
                },
                'code': 403,
                'assert': b''
            }, {
                'route': f'/p/{self.private_project1.id}/edit',
                'data': {
                    'year': 2017,
                    'make': 'Ford',
                    'model': 'Mustang',
                    'model_id': 69569,
                    'name': 'Mustang',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3700,
                    'drivetrain': 'RWD',
                    'engine_size': 5.0
                },
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete(self):
        with self.client as client:
            resp = client.get(
                f'/p/{self.public_project1.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.public_project1, self.public_user1.projects)

            resp = client.get(
                f'/p/{self.public_project2.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 403)
            self.assertIn(self.public_project2, self.public_user2.projects)

            resp = client.get(
                f'/p/{self.private_project1.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 403)
            self.assertIn(self.private_project1, self.private_user1.projects)

    def test_add_mod(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 200,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project2.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

            self.assertIn('Test Mod', self.public_project1.mods)
            self.assertNotIn('Test Mod', self.public_project2.mods)
            self.assertNotIn('Test Mod', self.private_project2.mods)

    def test_delete_mod(self):
        with self.client as client:
            resp = client.delete(f'/p/{self.public_project1.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('This is mod1', self.public_project1.mods)

            resp = client.delete(f'/p/{self.public_project2.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 403)
            self.assertIn('This is mod1', self.public_project2.mods)

            resp = client.delete(f'/p/{self.private_project1.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 403)
            self.assertIn('This is mod1', self.private_project1.mods)

    def test_new_update(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 200,
                'assert': b'<span class="h5">Test Update</span>'
            },
            {
                'route': f'/p/{self.public_project2.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_edit_update(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit-update/{self.public_project1.updates[0].id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 200,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project2.id}/edit-update/{self.public_project2.updates[0].id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/edit-update/{self.private_project1.updates[0].id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 403,
                'assert': b''
            },
        ]

        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete_update(self):
        with self.client as client:
            resp = client.get(
                f'/p/{self.public_project1.id}/delete-update/{self.public_project1_update.id}')
            self.assertNotIn(self.public_project1_update,
                             self.public_project1.updates)

            resp = client.get(
                f'/p/{self.public_project2.id}/delete-update/{self.public_project2_update.id}')
            self.assertIn(self.public_project2_update,
                          self.public_project2.updates)

            resp = client.get(
                f'/p/{self.private_project1.id}/delete-update/{self.private_project1_update.id}')
            self.assertIn(self.private_project1_update,
                          self.private_project1.updates)

    def test_new_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/new-comment',
                'data': {'content': 'Test comment'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test comment</p>'
            }, {
                'route': f'/p/{self.public_project2.id}/new-comment',
                'data': {'content': 'Test comment1'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test comment1</p>'
            },
            {
                'route': f'/p/{self.private_project1.id}/new-comment',
                'data': {'content': 'Test comment'},
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_edit_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit-comment/{self.public_project1_comment1.id}',
                'data': {'content': 'Test edit comment'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test edit comment</p>'
            },
            {
                'route': f'/p/{self.public_project1.id}/edit-comment/{self.public_project1_comment2.id}',
                'data': {'content': 'Test comment'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project2.id}/edit-comment/{self.public_project2_comment1.id}',
                'data': {'content': 'Test edit comment2'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test edit comment2</p>'
            },
            {
                'route': f'/p/{self.public_project2.id}/edit-comment/{self.public_project2_comment2.id}',
                'data': {'content': 'Test edit comment2'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project2.id}/edit-comment/{self.private_project2_comment.id}',
                'data': {'content': 'Test comment'},
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/delete-comment/{self.public_project1_comment1.id}',
                'code': 200,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project1.id}/delete-comment/{self.public_project1_comment2.id}',
                'code': 200,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project2.id}/delete-comment/{self.public_project2_comment1.id}',
                'code': 200,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project2.id}/delete-comment/{self.public_project2_comment2.id}',
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project2.id}/delete-comment/{self.private_project2_comment.id}',
                'code': 403,
                'assert': b''
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

            self.assertNotIn(self.public_project1_comment1,
                             self.public_project1.comments)
            self.assertNotIn(self.public_project1_comment2,
                             self.public_project1.comments)

            self.assertNotIn(self.public_project2_comment1,
                             self.public_project2.comments)
            self.assertIn(self.public_project2_comment2,
                          self.public_project2.comments)
            self.assertIn(self.private_project2_comment,
                          self.private_project2.comments)


class TestWithPrivateUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        seed_all(self)
        self.client = self.app.test_client(user=self.private_user1)

    def test_routes(self):

        test_data = [
            {
                'route': '/p/new',
                'code': 200,
                'assert': b'<h1>New Project</h1>'
            },
            # own project
            {
                'route': f'/p/{self.private_project1.id}',
                'code': 200,
                'assert': b'<h1 class="d-inline">PrivateProject1</h1>'
            },
            {
                'route': f'/p/{self.private_project1.id}/edit',
                'code': 200,
                'assert': b'<h1>Edit Project</h1>'},
            # public project
            {
                'route': f'/p/{self.public_project2.id}',
                'code': 200,
                'assert': b'<h1 class="d-inline">PublicProject2</h1>'
            },
            {
                'route': f'/p/{self.public_project2.id}/edit',
                'code': 403,
                'assert': b''
            },
            # private project
            {
                'route': f'/p/{self.private_project2.id}',
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project2.id}/edit',
                'code': 403,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

    def test_new(self):
        test_data = [
            {
                'data': {
                    'year': 2007,
                    'make': 'Ford',
                    'model': 'GT500',
                    'model_id': 15175,
                    'name': 'Shelby2',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3900,
                    'drivetrain': 'RWD',
                    'engine_size': 5.4
                },
                'code': 200,
                'assert': b'<h1 class="d-inline">Shelby2</h1>'
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, '/p/new', test)

    def test_edit(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit',
                'data': {
                    'year': 2017,
                    'make': 'Ford',
                    'model': 'Pinto',
                    'model_id': 69569,
                    'name': 'Mustang',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3700,
                    'drivetrain': 'RWD',
                    'engine_size': 5.0
                },
                'code': 403,
                'assert': b''
            }, {
                'route': f'/p/{self.private_project2.id}/edit',
                'data': {
                    'year': 2017,
                    'make': 'Ford',
                    'model': 'Pinto',
                    'model_id': 69569,
                    'name': 'Mustang',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3700,
                    'drivetrain': 'RWD',
                    'engine_size': 5.0
                },
                'code': 403,
                'assert': b''
            }, {
                'route': f'/p/{self.private_project1.id}/edit',
                'data': {
                    'year': 2017,
                    'make': 'Ford',
                    'model': 'Pinto',
                    'model_id': 69569,
                    'name': 'Mustang',
                    'private': 'PUBLIC',
                    'horsepower': 500,
                    'torque': 500,
                    'weight': 3700,
                    'drivetrain': 'RWD',
                    'engine_size': 5.0
                },
                'code': 200,
                'assert': b'alert-info">Project Successfully edited</div>'
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)
            self.assertEqual('Pinto', self.private_project1.model)
            self.assertNotEqual('Pinto', self.private_project2.model)
            self.assertNotEqual('Pinto', self.public_project2.model)

    def test_delete(self):
        with self.client as client:
            resp = client.get(
                f'/p/{self.public_project1.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 403)
            self.assertIn(self.public_project1, self.public_user1.projects)

            resp = client.get(
                f'/p/{self.private_project2.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 403)
            self.assertIn(self.public_project2, self.public_user2.projects)

            resp = client.get(
                f'/p/{self.private_project1.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.private_project1,
                             self.private_user1.projects)

    def test_add_mod(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project2.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/add-mod',
                'data': {'mod': 'Test Mod'},
                'code': 200,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

            self.assertIn('Test Mod', self.private_project1.mods)
            self.assertNotIn('Test Mod', self.public_project2.mods)
            self.assertNotIn('Test Mod', self.private_project2.mods)

    def test_delete_mod(self):
        with self.client as client:
            resp = client.delete(f'/p/{self.public_project1.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 403)
            self.assertIn('This is mod1', self.public_project1.mods)

            resp = client.delete(f'/p/{self.private_project2.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 403)
            self.assertIn('This is mod1', self.private_project2.mods)

            resp = client.delete(f'/p/{self.private_project1.id}/delete-mod/0')
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('This is mod1', self.private_project1.mods)

    def test_new_update(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project2.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/new-update',
                'data': {
                    'title': 'Test Update',
                    'content': 'Update content'
                },
                'code': 200,
                'assert': b'<span class="h5">Test Update</span>'
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_edit_update(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit-update/{self.public_project1_update.id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project2.id}/edit-update/{self.private_project2_update.id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/edit-update/{self.private_project1_update.id}',
                'data':
                    {
                        'title': 'Edited Update',
                        'content': 'This is content'
                    },
                'code': 200,
                'assert': b''
            },
        ]

        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete_update(self):
        with self.client as client:
            resp = client.get(
                f'/p/{self.public_project1.id}/delete-update/{self.public_project1_update.id}')
            self.assertIn(self.public_project1_update,
                          self.public_project1.updates)

            resp = client.get(
                f'/p/{self.private_project2.id}/delete-update/{self.private_project2_update.id}')
            self.assertIn(self.private_project2_update,
                          self.private_project2.updates)

            resp = client.get(
                f'/p/{self.private_project1.id}/delete-update/{self.private_project1_update.id}')
            self.assertNotIn(self.private_project1_update,
                             self.private_project1.updates)

    def test_new_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/new-comment',
                'data': {'content': 'Test comment'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test comment</p>'
            }, {
                'route': f'/p/{self.private_project2.id}/new-comment',
                'data': {'content': 'Test comment1'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/new-comment',
                'data': {'content': 'Test comment'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test comment</p>'
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_edit_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/edit-comment/{self.public_project1_comment3.id}',
                'data': {'content': 'Test edit comment'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test edit comment</p>'
            },
            {
                'route': f'/p/{self.public_project1.id}/edit-comment/{self.public_project1_comment2.id}',
                'data': {'content': 'Test comment'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project2.id}/edit-comment/{self.private_project2_comment.id}',
                'data': {'content': 'Test edit comment2'},
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/edit-comment/{self.private_project1_comment.id}',
                'data': {'content': 'Test edit comment2'},
                'code': 200,
                'assert': b'<p class="ms-2 mb-0">Test edit comment2</p>'
            }
        ]
        with self.client as client:
            for test in test_data:
                self.check_post_request(client, test['route'], test)

    def test_delete_comment(self):
        test_data = [
            {
                'route': f'/p/{self.public_project1.id}/delete-comment/{self.public_project1_comment3.id}',
                'code': 200,
                'assert': b''
            },
            {
                'route': f'/p/{self.public_project1.id}/delete-comment/{self.public_project1_comment2.id}',
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project2.id}/delete-comment/{self.private_project2_comment.id}',
                'code': 403,
                'assert': b''
            },
            {
                'route': f'/p/{self.private_project1.id}/delete-comment/{self.private_project1_comment.id}',
                'code': 200,
                'assert': b''
            },
        ]
        with self.client as client:
            for test in test_data:
                self.check_get_request(client, test['route'], test)

            self.assertNotIn(self.public_project1_comment3,
                             self.public_project1.comments)
            self.assertNotIn(self.private_project1_comment,
                             self.private_project1.comments)

            self.assertIn(self.public_project1_comment2,
                          self.public_project1.comments)
            self.assertIn(self.private_project2_comment,
                          self.private_project2.comments)
