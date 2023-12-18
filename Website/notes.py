from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Note
from . import db

notes = Blueprint('notes', __name__)

@notes.route('/')
@login_required
def note_nav():
    return render_template('notes/note_nav.html')

@notes.route('/add', methods=['GET', 'POST'])
@login_required
def add_note():
    user_id = current_user.user_id
    if request.method == 'POST':
        title = request.form['noteTitle']
        note = request.form['note']
        new_note = Note(user_id=user_id, title=title, content=note)

        db.session.add(new_note)
        db.session.commit()
    return render_template('notes/add_note.html',)

@notes.route('/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.user_id:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.list_notes'))

@notes.route('/edit/<int:note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.user_id:
        abort(403)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
    return redirect(url_for('notes.detail_note', note_id=note_id))

@notes.route('/<int:note_id>', methods=['GET', 'POST'])
@login_required
def detail_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.user_id:
        abort(403)
    else:
        return render_template('notes/note.html', note=note)

@notes.route('/list')
@login_required
def list_notes():
    user_id = current_user.user_id
    notes = Note.query.filter_by(user_id=user_id).all()
    return render_template('notes/list_notes.html', notes=notes)