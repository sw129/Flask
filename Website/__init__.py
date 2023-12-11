from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "jdusioahuoiyhuiqwsdoi iyhudsoa"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1975@localhost:5432/testdatabase'
    db.init_app(app)

    # Create database within app context
    # with app.app_context():
    #     db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .auth import auth
    from .home import home
    from .notes import notes
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(notes, url_prefix='/notes/')

    return app