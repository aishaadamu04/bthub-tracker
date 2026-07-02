from flask import render_template, session, redirect, url_for, request
from datetime import datetime
from . import student_bp
from ..database.db import query_db, execute_db
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

    # update last_active every time the dashboard loads
    execute_db(
        "UPDATE children SET last_active = ? WHERE id = ?",
        [datetime.now(), child['id']]
    )

    level_info = CURRICULUM_LEVELS.get(child['current_level'], {})
    week_number = child['current_level']

    progress = query_db(
        "SELECT * FROM progress WHERE child_id = ? AND week_number = ?",
        [child['id'], week_number]
    )

    completed_titles = [p['lesson_title'] for p in progress if p['completed']]
    topics = level_info.get('topics', [])
    all_lessons_done = len(topics) > 0 and all(t in completed_titles for t in topics)

    # has this child already passed the quiz for this level?
    passed_attempt = query_db(
        "SELECT * FROM quiz_attempts WHERE child_id = ? AND week_number = ? AND passed = True",
        [child['id'], week_number], one=True
    )

    return render_template('student/dashboard.html',
                            child=child,
                            level_info=level_info,
                            week_number=week_number,
                            topics=topics,
                            completed_titles=completed_titles,
                            all_lessons_done=all_lessons_done,
                            passed_attempt=passed_attempt)


@student_bp.route('/lesson/toggle', methods=['POST'])
@login_required
def toggle_lesson():
    child_id = session['user_id']
    week_number = request.form.get('week_number', type=int)
    lesson_title = request.form.get('lesson_title')

    existing = query_db(
        "SELECT * FROM progress WHERE child_id = ? AND week_number = ? AND lesson_title = ?",
        [child_id, week_number, lesson_title], one=True
    )

    if existing:
        new_status = not existing['completed']
        execute_db(
            "UPDATE progress SET completed = ?, completed_at = ? WHERE id = ?",
            [new_status, datetime.now() if new_status else None, existing['id']]
        )
    else:
        execute_db(
            "INSERT INTO progress (child_id, week_number, lesson_title, completed, completed_at) VALUES (?, ?, ?, ?, ?)",
            [child_id, week_number, lesson_title, True, datetime.now()]
        )

    return redirect(url_for('student.dashboard'))


@student_bp.route('/quiz/<int:week_number>', methods=['GET', 'POST'])
@login_required
def quiz(week_number):
    child = query_db(
        "SELECT * FROM children WHERE id = ?",
        [session['user_id']], one=True
    )
    level_info = CURRICULUM_LEVELS.get(week_number, {})
    questions = query_db(
        "SELECT * FROM quiz_questions WHERE week_number = ?",
        [week_number]
    )

    if request.method == 'POST':
        score = 0
        for q in questions:
            submitted = request.form.get(f"q_{q['id']}")
            if submitted == q['correct_option']:
                score += 1

        total = len(questions)
        percent = round((score / total) * 100) if total > 0 else 0
        unlock_score = level_info.get('unlock_score', 100)
        passed = percent >= unlock_score

        execute_db(
            """INSERT INTO quiz_attempts (child_id, week_number, score, total_questions, passed)
               VALUES (?, ?, ?, ?, ?)""",
            [child['id'], week_number, percent, total, passed]
        )

        if passed and child['current_level'] == week_number:
            next_level = week_number + 1
            if next_level in CURRICULUM_LEVELS:
                execute_db(
                    "UPDATE children SET current_level = ? WHERE id = ?",
                    [next_level, child['id']]
                )

        return render_template('student/quiz_result.html',
                                score=percent, passed=passed,
                                unlock_score=unlock_score,
                                level_info=level_info)

    return render_template('student/quiz.html',
                            questions=questions, level_info=level_info,
                            week_number=week_number)