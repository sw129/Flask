from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

login_manager = LoginManager()
db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    app.config['SECRET_KEY'] = "jdusioahuoiyhuiqwsdoi iyhudsoa"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1975@localhost:5432/testdatabase'
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .auth import auth
    from .home import home
    from .notes import notes
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(notes, url_prefix='/notes/')

    return app

@app.context_processor
def add_base_params():
  return dict(user_is_authenticated=current_user.is_authenticated)
