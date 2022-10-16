# app > __init__.py

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dropzone import Dropzone
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_moment import Moment

db = SQLAlchemy()
lm = LoginManager()
dz = Dropzone()
csrf = CSRFProtect()
moment = Moment()


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')

    # toolbar = DebugToolbarExtension(app)

    lm.login_view = 'login'

    db.init_app(app)
    lm.init_app(app)
    dz.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)

    with app.app_context():

        # initialize SQLalchemy models
        from . import models

        @app.errorhandler(CSRFError)
        def handle_csrf_error(e):
            return e.description, 400

        from . import routes
        from .project import bp as project_bp
        from .profile import bp as profile_bp

        app.register_blueprint(profile_bp, url_prefix='/u')
        app.register_blueprint(project_bp, url_prefix='/p')

        # db.drop_all()
        db.create_all()

        return app
