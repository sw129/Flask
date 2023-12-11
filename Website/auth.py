from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user
from . import db, login_manager
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        new_user = User(name=name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            #session['user_id'] = user.user_id
            login_user(user)
            return redirect('/notes')
        else:
            return 'Неверный логин или пароль'
    return render_template('login.html')

@auth.route('/logout')
def logout():
    #session.pop('user_id', None)
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)
