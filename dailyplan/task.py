from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dailyplan.auth import login_required
from dailyplan.db import get_db
from dailyplan.date import date_to_text, add_suffix

from datetime import date, datetime, timedelta
import time

bp = Blueprint('task', __name__)

@bp.route('/')
@login_required
def index():
	db = get_db()
	url_date = date_to_text(date.today().strftime('%m/%d/%Y'))
	
	tasks = db.execute(
		'SELECT t.id, task_text, created, user_id, email'
		' FROM task t JOIN user u ON t.user_id = u.id'
		' ORDER by created DESC'
	).fetchall()
	return render_template('task/index.html', tasks=tasks, url_date=url_date)

@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
	if request.method == 'POST':
		task_text = request.form['task_text']
		error = None

		if not task_text:
			error = "Task is required."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO task (task_text, user_id)'
				' VALUES (?, ?)',
				(task_text, g.user['id'])
			)
			db.commit()
			return redirect(url_for('task.index'))

	return	render_template('task/new.html')


def get_task(id, check_user =True):
	task = get_db().execute(
		'SELECT t.id, created, task_text, user_id, email'
		' FROM task t JOIN user u ON t.user_id = u.id'
		' WHERE t.id = ?',
		(id,)
	).fetchone()

	if task is None:
		abort(404, f'Task id {id} doesn\'t exist.')

	if check_user and task['user_id'] != g.user['id']:
		abort(403)

	return task

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
	task = get_task(id)

	if request.method == "POST":
		task_text = request.form['task_text']
		error = None

		if not task_text:
			error = "Task is required."

		if error is not None:
			flash(error)

		else:
			db = get_db()
			db.execute(
				'UPDATE task SET task_text = ?'
				' WHERE id = ?',
				(task_text, id)
			)
			db.commit()
			return redirect(url_for('task.index'))

	return render_template('/task/update.html', task=task)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	get_task(id)
	db = get_db()
	db.execute('DELETE FROM task WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('task.index'))