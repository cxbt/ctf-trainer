from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth import login_required, admin_required
from flaskr.db import get_db


bp = Blueprint('challenge', __name__, url_prefix='/challenge')


@bp.route('/', methods=('GET',))
@login_required
def index():
    db = get_db()
    if g.user:
        challenges = db.execute(
            'SELECT c.id, c.title, c.body, c.attachment , c.thumbsup, c.score, r.timestamp'
            ' FROM challenge AS c'
            ' LEFT JOIN records AS r ON (c.id = r.challengeid)'
            ' AND (r.userid = ?)'
            ' ORDER BY created DESC',
            (g.user['id'],)
        ).fetchall()
    else:
        challenges = db.execute(
            'SELECT c.id, c.title, c.body, c.thumbsup, c.score'
            ' FROM challenge AS c'
            ' ORDER BY created DESC'
        ).fetchall()

    return render_template('chall/index.html', challenges=challenges)


@bp.route('/<int:id>', methods=('POST',))
@login_required
def authenticate(id):
    db = get_db()
    challenge = db.execute(
        'SELECT id, flag, score'
        ' FROM challenge'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    error = None

    if challenge is None:
        error = f'There is no challenge number {id}!'

    if error is not None:
        flash(error)
        return redirect(url_for('challenge.index'))

    flag = request.form['flag']

    if not check_password_hash(challenge['flag'], flag):
        flash(f'You are wrong :(')
        return redirect(url_for('challenge.index'))

    db.execute(
        'INSERT INTO records (userid, challengeid) VALUES (?, ?)',
        (g.user['id'], id)
    )
    db.execute(
        'UPDATE user'
        ' SET score=?'
        ' WHERE id = ?',
        (int(g.user['score']) + int(challenge['score']), g.user['id'])
    )
    db.commit()
    flash(f'Whohoo, Correct!')
    return redirect(url_for('challenge.index'))
