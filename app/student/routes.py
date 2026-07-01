from flask import render_template, session, redirect, url_for
from . import student_bp
from ..database.db import query_db
from ..models.progress import CURRICULUM_LEVELS


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@student_bp.route('/dashboard')
@login_required
def dashboard():
    child = query_db(
        "SELECT * FROM children WHERE id = ?",
        [session['user_id']], one=True
    )
    level_info = CURRICULUM_LEVELS.get(child['current_level'], {})
    progress = query_db(
        "SELECT * FROM progress WHERE child_id = ?",
        [child['id']]
    )

    return render_template('student/dashboard.html',
                           child=child,
                           level_info=level_info,
                           progress=progress)