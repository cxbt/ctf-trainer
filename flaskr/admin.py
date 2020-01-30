from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

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
            return redirect(url_for('admin.index'))

    return render_template('admin/challenge-new.html')
