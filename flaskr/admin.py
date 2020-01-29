from flask import (
    Blueprint, g, render_template, url_for
)

from flaskr.auth import login_required, admin_required
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@login_required
@admin_required
@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/index.html')