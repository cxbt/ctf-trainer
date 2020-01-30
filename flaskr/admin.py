from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash


from flaskr.auth import login_required, admin_required
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@login_required
@admin_required
@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/index.html')


@login_required
@admin_required
@bp.route('/challenge', methods=('GET',))
def list_challenge():
    db = get_db()
    challenges = db.execute(
        'SELECT id, title, body, created, thumbsup, score'
        ' FROM challenge'
        ' ORDER BY created ASC'
    ).fetchall()
    return render_template('admin/challenge-list.html', challenges=challenges)


@login_required
@admin_required
@bp.route('/challenge/create', methods=('GET', 'POST'))
def create_challenge():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        flag = request.form['flag']
        score = request.form['score']
        error = None

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
        else:
            db = get_db()
            db.execute(
                'INSERT INTO challenge (title, body, thumbsup, flag, score)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, 0, generate_password_hash(flag), score)
            )
            db.commit()
            flash(f'Successfully created challenge "{title}"!"')
            return redirect(url_for('admin.list_challenge'))

    return render_template('admin/challenge-new.html')


@login_required
@admin_required
@bp.route('/challenge/edit/<int:id>', methods=('GET', 'POST'))
def edit_challenge(id):
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

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        flag = request.form['flag']
        score = request.form['score']
        error = None

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
        else:
            db = get_db()
            db.execute(
                'UPDATE challenge'
                ' SET title=?, body=?, flag=?, score=?'
                ' WHERE id = ?',
                (title, body, generate_password_hash(flag), score, id)
            )
            db.commit()
            flash(f'Successfully edited challenge "{title}"!')
            return redirect(url_for('admin.list_challenge'))

    return render_template('admin/challenge-edit.html', challenge=challenge)


@login_required
@admin_required
@bp.route('/challenge/delete/<int:id>', methods=('POST',))
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
