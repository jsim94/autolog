from app import models
from app.models.images import ProjectPicture


def seed_users(c: object):
    ''' Seeds users into database for testing
    :param c: must be self
    '''
    models.User.query.delete()

    c.public_user1 = models.User.signup(
        username='public_user1',
        email='public_user1@test.com',
        password='Password'
    )

    c.public_user2 = models.User.signup(
        username='public_user2',
        email='public_user2@test.com',
        password='Password'
    )

    c.private_user1 = models.User.signup(
        username='private_user1',
        email='private_user1@test.com',
        password='Password'
    )
    c.private_user1.edit(private='PRIVATE')

    c.private_user2 = models.User.signup(
        username='private_user2',
        email='private_user2@test.com',
        password='Password'
    )
    c.private_user2.edit(private='PRIVATE')


def seed_projects(c: object):
    '''Seeds projects into database for testing. Must call 'seed_users(self)' before this function

    :param c: must be self
    '''
    models.Project.query.delete()

    c.public_project1 = models.Project.create(
        user_pk=c.public_user1.pk,
        name='PublicProject1',
        description='This is PublicProject1',
        model_id=15175,
        private='PUBLIC',
        year=2007,
        make='Ford',
        model='GT 500',
        horsepower=500,
        torque=490,
        weight=3900,
        drivetrain='RWD',
        engine_size=5.4
    )
    c.public_project2 = models.Project.create(
        user_pk=c.public_user2.pk,
        name='PublicProject2',
        description='This is PublicProject2',
        model_id=69569,
        private='PUBLIC',
        year=2017,
        make='Ford',
        model='Mustang',
        horsepower=435,
        torque=400,
        weight=3700,
        drivetrain='RWD',
        engine_size=5.0
    )
    c.private_project1 = models.Project.create(
        user_pk=c.private_user1.pk,
        name='PrivateProject1',
        description='This is PrivateProject1',
        model_id=69569,
        private='PRIVATE',
        year=1992,
        make='Ford',
        model='Mustang',
        horsepower=105,
        torque=135,
        weight=3300,
        drivetrain='RWD',
        engine_size=2.3
    )
    c.private_project2 = models.Project.create(
        user_pk=c.private_user2.pk,
        name='PrivateProject2',
        description='This is PrivateProject2',
        model_id=5962,
        private='PRIVATE',
        year=2003,
        make='Buick',
        model='LeSabre',
        horsepower=205,
        torque=229,
        weight=3564,
        drivetrain='FWD',
        engine_size=3.8
    )

    c.public_project1.add_mod('This is mod1')
    c.public_project2.add_mod('This is mod1')
    c.private_project1.add_mod('This is mod1')
    c.private_project2.add_mod('This is mod1')

    # UPDATES
    c.public_project1_update = models.Update.create(
        project_id=c.public_project1.id,
        title='This is title',
        content='This is an update'
    )
    c.public_project2_update = models.Update.create(
        project_id=c.public_project2.id,
        title='This is title',
        content='This is an update'
    )
    c.private_project1_update = models.Update.create(
        project_id=c.private_project1.id,
        title='This is title',
        content='This is an update'
    )
    c.private_project2_update = models.Update.create(
        project_id=c.private_project2.id,
        title='This is title',
        content='This is an update'
    )

    # COMMENTS
    # public
    # project 1
    c.public_project1_comment1 = models.Comment.create(
        user_id=c.public_user1.id,
        project_id=c.public_project1.id,
        content='This is a comment'
    )
    c.public_project1_comment2 = models.Comment.create(
        user_id=c.public_user2.id,
        project_id=c.public_project1.id,
        content='This is a comment'
    )
    c.public_project1_comment3 = models.Comment.create(
        user_id=c.private_user1.id,
        project_id=c.public_project1.id,
        content='This is a comment'
    )
    c.public_project1_comment4 = models.Comment.create(
        user_id=c.private_user2.id,
        project_id=c.public_project1.id,
        content='This is a comment'
    )

    # project2
    c.public_project2_comment1 = models.Comment.create(
        user_id=c.public_user1.id,
        project_id=c.public_project2.id,
        content='This is a comment'
    )
    c.public_project2_comment2 = models.Comment.create(
        user_id=c.public_user2.id,
        project_id=c.public_project2.id,
        content='This is a comment'
    )
    c.public_project2_comment3 = models.Comment.create(
        user_id=c.private_user1.id,
        project_id=c.public_project2.id,
        content='This is a comment'
    )
    c.public_project2_comment4 = models.Comment.create(
        user_id=c.private_user2.id,
        project_id=c.public_project2.id,
        content='This is a comment'
    )

    # private
    c.private_project1_comment = models.Comment.create(
        user_id=c.private_user1.id,
        project_id=c.private_project1.id,
        content='This is a comment'
    )
    c.private_project2_comment = models.Comment.create(
        user_id=c.private_user2.id,
        project_id=c.private_project2.id,
        content='This is a comment'
    )


def seed_all(c):
    seed_users(c=c)
    seed_projects(c=c)

    comment_data = [
        {
            'user_id': c.public_user1.id,
            'project_id': c.public_project1.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.public_user2.id,
            'project_id': c.public_project1.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.private_user1.id,
            'project_id': c.public_project1.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.private_user2.id,
            'project_id': c.public_project1.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.public_user1.id,
            'project_id': c.public_project2.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.public_user2.id,
            'project_id': c.public_project2.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.private_user1.id,
            'project_id': c.public_project2.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.private_user2.id,
            'project_id': c.public_project2.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.private_user1.id,
            'project_id': c.private_project1.id,
            'content': 'This is a comment'
        },
        {
            'user_id': c.private_user2.id,
            'project_id': c.private_project2.id,
            'content': 'This is a comment'
        },
    ]

    for comment in comment_data:
        models.Comment.create(**comment)
