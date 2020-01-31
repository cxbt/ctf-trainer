from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

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


@login_required
@bp.route('/challenge/<int:id>', methods=('POST',))
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
        flash(f'NOPE')
        return redirect(url_for('challenge.index'))
    
    db.execute(
        'UPDATE user'
        ' SET score=?'
        ' WHERE id = ?',
        (int(challenge['score']), g.user['id'])
    )
    db.commit()
    flash(f'CORRECT!')
    return redirect(url_for('challenge.index'))
