from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from ..database.db import query_db, execute_db
from ..auth.forms import ParentRegistrationForm, ChildRegistrationForm, LoginForm
@auth_bp.route('/register/parent', methods=['GET', 'POST'])
def register_parent():
    if request.method== "POST":
        form = ParentRegistrationForm(request.form) 
        is_valid, errors = form.validate()

        if not is_valid:
            return render_template("auth/register_parent.html", errors=errors)
        
        existing = query_db(
            "SELECT id FROM parents WHERE email = ?",
            [form.email],
            one=True)
        
        if existing:
            errors.append("Email already registered")
            return render_template("auth/register_parent.html", errors=errors)
        
        hashed_password = generate_password_hash(form.password)

        execute_db(
            "INSERT INTO parents (full_name, phone_number, email, password_hash) VALUES (?, ?, ?, ?)",
            [form.full_name, form.phone_number, form.email, hashed_password]
        )

        return redirect(url_for("auth.login"))
    return redirect(url_for('auth.register_parent'))
    #return render_template('auth/register_parent.html', errors=[])


@auth_bp.route('/register/child', methods=['GET', 'POST'])
def register_child():
    if request.method == 'POST':
        form = ChildRegistrationForm(request.form)
        is_valid, errors = form.validate()

        if not is_valid:
            return render_template('auth/register_child.html', errors=errors)

        parent = query_db(
            "SELECT id FROM parents WHERE phone_number = ?",
            [form.parent_phone], one=True
        )
        if not parent:
            return render_template('auth/register_child.html',
                                   errors=["No parent account with that phone number"])

        existing = query_db(
            "SELECT id FROM children WHERE username = ?",
            [form.username], one=True
        )
        if existing:
            return render_template('auth/register_child.html',
                                   errors=["Username already taken"])

        hashed_password = generate_password_hash(form.password)
        execute_db(
            "INSERT INTO children (full_name, username, password_hash, parent_phone) VALUES (?,?,?,?)",
            [form.full_name, form.username, hashed_password, form.parent_phone]
        )
        return redirect(url_for('auth.login'))

    return render_template('auth/register_child.html', errors=[])


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        is_valid, errors = form.validate()

        if not is_valid:
            return render_template('auth/login.html', errors=errors)

        if form.user_type == 'parent':
            user = query_db(
                "SELECT * FROM parents WHERE email = ?",
                [form.identifier], one=True
            )
            if not user or not check_password_hash(user['password_hash'], form.password):
                return render_template('auth/login.html',
                                       errors=["Invalid email or password"])
            session['user_id'] = user['id']
            session['user_type'] = 'parent'
            return redirect(url_for('parent.dashboard'))

        else:
            user = query_db(
                "SELECT * FROM children WHERE username = ?",
                [form.identifier], one=True
            )
            if not user or not check_password_hash(user['password_hash'], form.password):
                return render_template('auth/login.html',
                                       errors=["Invalid username or password"])
            session['user_id'] = user['id']
            session['user_type'] = 'child'
            return redirect(url_for('student.dashboard'))

    return render_template('auth/login.html', errors=[])


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))