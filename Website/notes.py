from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

notes = Blueprint('notes', __name__)

@notes.route('/', methods=['GET', 'POST'])
@login_required
def register():
    user_id = current_user.user_id
    if request.method == 'POST':
        title = request.form['noteTitle']
        note = request.form['note']
        new_note = Note(user_id=user_id, title=title, content=note)

        db.session.add(new_note)
        db.session.commit()

        return redirect('/notes/')
    notes = Note.query.filter_by(user_id=user_id).all()
    return render_template('notes.html', notes=notes)