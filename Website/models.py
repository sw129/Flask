from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column('password', db.String(200), nullable=False)

    @property
    def password(self):
        raise AttributeError('пароль не является читаемым атрибутом')

    @password.setter
    def password(self, raw_password):
        self._password_hash = generate_password_hash(raw_password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def get_id(self):
        return self.user_id

class Note(db.Model):
    __tablename__ = "notes"

    note_id = db.Column('notes_id', db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)