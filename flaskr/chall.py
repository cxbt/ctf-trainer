from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from flaskr.auth import login_required, admin_required
from flaskr.db import get_db


bp = Blueprint('challenge', __name__)


@bp.route('/')
def index():
    db = get_db()
    challenges = db.execute(
        'SELECT id, title, body, created, thumbsup, score'
        ' FROM challenge'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('chall/index.html', challenges=challenges)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@admin_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        flag = request.form['flag']
        score = request.form['score']
        error = None

        if not title:
            error = 'Title is required.'

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
            return redirect(url_for('chall.index'))

    return render_template('chall/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
@admin_required
def update(id):
    challenge = get_challenge(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        score = request.form['score']
        error = None

        if not title:
            error = 'Title is required.'

        try:
            int(score)
        except ValueError:
            error = 'Score should be numeric.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE challenge SET title = ?, body = ?, score = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('chall.index'))

    return render_template('chall/update.html', challenge=challenge)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@admin_required
def delete(id):
    get_challenge(id)
    db = get_db()
    db.execute('DELETE FROM challenge WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('chall.index'))


def get_challenge(id, check_admin=True):
    challenge = get_db().execute(
        'SELECT id, title, body, created, thumbsup, score'
        ' FROM challenge'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if challenge is None:
        abort(404, "Challenge id {0} doesn't exist.".format(id))

    if check_admin and g.user['isAdmin'] == False:
        abort(403)

    return challenge
