# app > __init__.py
import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_dropzone import Dropzone
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_moment import Moment

lm = LoginManager()
dz = Dropzone()
csrf = CSRFProtect()
moment = Moment()


def create_app():

    app = Flask(__name__)

    config_obj = os.environ.get('FLASK_CONFIG', 'config.ProdConfig')
    print(f'Starting app with config: \'{config_obj}\'')
    try:
        app.config.from_object(config_obj)
    except ImportError as e:
        err_msg = f'Invalid env config value \'{config_obj}\''
        raise ImportError(err_msg) from e

    # create upload directory if non-existent
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
        print('Created user upload directory:',
              app.config['UPLOAD_FOLDER'])

    toolbar = DebugToolbarExtension(app)

    # initialize SQLalchemy
    from .models import db
    db.init_app(app)

    lm.login_view = 'root.login'
    lm.init_app(app)
    dz.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)

    with app.app_context():

        @app.errorhandler(CSRFError)
        def handle_csrf_error(e):
            return e.description, 400

        from .blueprints.root import bp as root_bp
        from .blueprints.project import bp as project_bp
        from .blueprints.profile import bp as profile_bp

        app.register_blueprint(root_bp, url_prefix='/')
        app.register_blueprint(profile_bp, url_prefix='/u')
        app.register_blueprint(project_bp, url_prefix='/p')

        db.create_all()
        return app
