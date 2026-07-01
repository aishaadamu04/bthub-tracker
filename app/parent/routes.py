from flask import render_template, session, redirect, url_for
from . import parent_bp
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


@parent_bp.route('/dashboard')
@login_required
def dashboard():
    parent = query_db(
        "SELECT * FROM parents WHERE id = ?",
        [session['user_id']], one=True
    )
    children = query_db(
        "SELECT * FROM children WHERE parent_phone = ?",
        [parent['phone_number']]
    )

    children_data = []
    for child in children:
        progress = query_db(
            "SELECT * FROM progress WHERE child_id = ?",
            [child['id']]
        )
        level_info = CURRICULUM_LEVELS.get(child['current_level'], {})
        children_data.append({
            'child': child,
            'level_info': level_info,
            'progress': progress
        })

    return render_template('parent/dashboard.html',
                           parent=parent,
                           children_data=children_data)