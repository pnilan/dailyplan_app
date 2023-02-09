import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import re

from dailyplan.db import get_db

# Creates blueprint 'auth' 
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = []

        


        if not name:
            error.append("Your name is required.")
        
        if not email:
            error.append('Email is required.')
        
        if not password:
            error.append('Password is required.')

        # No special characters in name, no leading spaces
        name_pattern = re.compile("^\w+( \w+)*$")
        name_validity = re.fullmatch(name_pattern, name)      
    
        if name_validity:
            print("Valid name.")
        else:
            print("Invalid name.")
            error.append("Name cannot contain special characters.")

        # Min password requirements: 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
        pw_pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$")
        pw_validity = re.search(pw_pattern, password)
            
        if pw_validity:
            print("Password is valid.")
        else:
            print('Password is invalid.')
            error.append("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")

        if error == []:
            try:
                db.execute(
                    "INSERT INTO user (name, email, password) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password)),
                )
                db.commit()

                user = db.execute(
                'SELECT * FROM user WHERE email = ?', (email,)
                ).fetchone()
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            except db.IntegrityError:
                error = ["Email is already registered."]
            else:
                return redirect(url_for("auth.login"))

        for n in error:
            flash(n)

    return render_template('auth/signup.html')

@bp.route('/login', methods=("GET", 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = "Incorrect email/password combo."
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect email/password combo.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            db.execute(
                "UPDATE user SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user['id'],)
            )
            db.commit()
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view



def  get_user(user_id, check_user=True):

    user  = get_db().execute(
        'SELECT id, name, email, dark_mode, week_view FROM user WHERE id = ?', (user_id,)).fetchone()

    if user is None: 
        abort(404, f'User doesn\'t exist.')

    if check_user and user['id'] != g.user['id']: 
        abort(403)

    print(user['name'])
    return user

@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    user = get_user(g.user['id'])

    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user_dark = request.form.get('user_dark_mode')
        user_week_view = request.form.get('user_week_view')
        error = None

        if not user_name:
            user_name = user['name']

        if not user_email:
            user_email = user['email']

        if not user_dark:
            user_dark = False
        else:
            user_dark = True

        if not user_week_view:
            user_week_view = False
        else:
            user_week_view = True

        if not user_password:
            db = get_db()
            db.execute(
                'UPDATE user SET name = ?, email = ?, dark_mode = ?, week_view = ? WHERE id = ?',
                (user_name, user_email, user_dark, user_week_view, g.user['id'])
            )
            db.commit()
            return redirect(url_for('index'))
    
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET name = ?, email = ?, password = ?, dark_mode = ?, week_view = ?'
                ' WHERE id = ?',
                (user_name, user_email, generate_password_hash(user_password), user_dark, user_week_view, g.user['id'])
            )
            db.commit()
        
            return redirect(request.referrer)






