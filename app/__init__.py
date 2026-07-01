from flask import Flask
from .config import Config
from .database.db import init_db


def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    init_db(app)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .parent import parent_bp
    app.register_blueprint(parent_bp, url_prefix='/parent')

    from .student import student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    from flask import redirect, url_for

    @app.route('/')
    def index():
     return redirect(url_for('auth.login'))

    return app
