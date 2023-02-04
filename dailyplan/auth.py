import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

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
		error = None

		if not name:
			error = "Your name is required."
		elif not email:
			error = 'Email is required.'
		elif not password:
			error = 'Password is required.'

		if error is None:
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
				error = f"Email {email} is already registered."
			else:
				return redirect(url_for("auth.login"))

		flash(error)

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
	return redirect(url_for('index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view



