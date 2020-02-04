from flask import (
    Blueprint, g, render_template, url_for
)

from flaskr.db import get_db


bp = Blueprint('rank', __name__, url_prefix='/rank')


@bp.route('/')
def index():
    db = get_db()
    record = db.execute(
        'SELECT u.username, u.score, r.timestamp, max(r.id)'
        ' FROM user AS u'
        ' INNER JOIN records AS r ON (u.id = r.userid)'
        ' GROUP BY r.userid HAVING max(r.id)'
        ' ORDER BY u.score DESC, r.timestamp ASC'
    ).fetchall()

    return render_template('rank/index.html', records=record)
