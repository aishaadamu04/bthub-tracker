#from app import create_app
from flask import Flask

def create_app():
    app = Flask(__name__)
    from app.student.routes import main_bp
    app.register_blueprint(main_bp)

    return app


# from app import create_app

# app = create_app('development')

# if __name__ == '__main__':
#     app.run(port=5001)