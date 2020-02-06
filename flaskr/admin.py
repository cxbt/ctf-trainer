import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask import current_app as app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from flaskr.auth import login_required, admin_required
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=('GET',))
@admin_required
def index():
    return render_template('admin/index.html')


@bp.route('/challenge', methods=('GET',))
@admin_required
def list_challenge():
    db = get_db()
    challenges = db.execute(
        'SELECT id, title, body, created, thumbsup, score'
        ' FROM challenge'
        ' ORDER BY created ASC'
    ).fetchall()
    return render_template('admin/challenge-list.html', challenges=challenges)


@bp.route('/challenge/create', methods=('GET', 'POST'))
@admin_required
def create_challenge():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        file = request.files['attachment']
        flag = request.form['flag']
        score = request.form['score']
        error = None

        # Required Field: Title, Flag, Score
        if not title:
            error = 'Title is required.'
        elif not flag:
            error = 'Flag is required.'

        try:
            int(score)
        except ValueError:
            error = 'Score should be numeric.'

        if error is not None:
            flash(error)

        import os
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        db = get_db()
        db.execute(
            'INSERT INTO challenge (title, body, attachment, thumbsup, flag, score)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (title, body, file.filename, 0, generate_password_hash(flag), score)
        )
        db.commit()
        flash(f'Successfully created challenge "{title}"!"')
        return redirect(url_for('admin.list_challenge'))

    return render_template('admin/challenge-new.html')


@bp.route('/challenge/edit/<int:id>', methods=('GET', 'POST'))
@admin_required
def edit_challenge(id):
    db = get_db()
    challenge = db.execute(
        'SELECT id, title, body, attachment, created, thumbsup, score'
        ' FROM challenge'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    error = None

    if not challenge:
        error = f"There is no challenge id {id}"

    if error is not None:
        flash(error)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        file = request.files['attachment']
        flag = request.form['flag']
        score = request.form['score']
        error = None

        # Required Field: Title, Flag, Score
        if not title:
            error = 'Title is required.'
        elif not flag:
            error = 'Flag is required.'

        try:
            int(score)
        except ValueError:
            error = 'Score should be numeric.'

        if error is not None:
            flash(error)

        # Not-required Field: Body, Attachment
        if not file.filename:
            file.filename = challenge['attachment']
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        db = get_db()
        db.execute(
            'UPDATE challenge'
            ' SET title=?, body=?, attachment=?, flag=?, score=?'
            ' WHERE id = ?',
            (title, body, file.filename, generate_password_hash(flag), score, id)
        )
        db.commit()
        flash(f'Successfully edited challenge "{title}"!')
        return redirect(url_for('admin.list_challenge'))

    return render_template('admin/challenge-edit.html', challenge=challenge)


@bp.route('/challenge/delete/<int:id>', methods=('GET',))
@admin_required
def delete_challenge(id):
    db = get_db()
    challenge = db.execute(
        'SELECT id, title, body, created, thumbsup, score'
        ' FROM challenge'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    error = None

    if not challenge:
        error = f"There is no challenge id {id}"

    if error is not None:
        flash(error)

    db.execute(
        'DELETE'
        ' FROM challenge'
        ' WHERE id = ?',
        (id,)
    )
    db.commit()
    flash('Successfully deleted!')
    return redirect(url_for('admin.list_challenge'))


@bp.route('/member')
@admin_required
def list_member():
    db = get_db()
    members = db.execute(
        'SELECT id, isAdmin, username, email, score'
        ' FROM user'
        ' ORDER BY id ASC'
    ).fetchall()

    return render_template('admin/member-list.html', members=members)


@bp.route('/member/delete/<int:id>')
@admin_required
def delete_member(id):
    db = get_db()
    member = db.execute(
        'SELECT id, isAdmin, username, email, score'
        ' FROM user'
        ' WHERE id = ?',
        (id, )
    ).fetchone()
    error = None

    if not member:
        error = f'There is no member id {id}.'

    if error is not None:
        flash(error)

    db.execute(
        'DELETE'
        ' FROM user'
        ' WHERE id = ?',
        (id,)
    )
    db.commit()
    flash(f'Successfully removed user {id}!')
    return redirect(url_for('admin.list_member'))
