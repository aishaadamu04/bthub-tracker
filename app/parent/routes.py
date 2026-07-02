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
        level_info = CURRICULUM_LEVELS.get(child['current_level'], {})
        week_number = child['current_level']

        progress = query_db(
            "SELECT * FROM progress WHERE child_id = ? AND week_number = ?",
            [child['id'], week_number]
        )

        topics = level_info.get('topics', [])
        total_lessons = len(topics)
        completed_lessons = len([p for p in progress if p['completed']])
        percent_complete = round((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

        latest_quiz = query_db(
            """SELECT * FROM quiz_attempts WHERE child_id = ? 
               ORDER BY attempted_at DESC LIMIT 1""",
            [child['id']], one=True
        )

        children_data.append({
            'child': child,
            'level_info': level_info,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'percent_complete': percent_complete,
            'latest_quiz': latest_quiz
        })

    return render_template('parent/dashboard.html',
                            parent=parent,
                            children_data=children_data)