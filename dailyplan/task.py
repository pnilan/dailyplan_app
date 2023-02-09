from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from dailyplan.auth import login_required, get_user
from dailyplan.db import get_db
from dailyplan.subtask import new
from dailyplan.date import date_to_text, add_suffix

from datetime import date, datetime, timedelta
import time
import re

bp = Blueprint('task', __name__)

@bp.route('/')
@login_required
def home():

	url_date = date.today().strftime("%m%d%y")
	return redirect(url_for('task.index', date=url_date))

@bp.route('/day/<date>', methods=('GET', 'POST'))
@login_required
def index(date):
	db = get_db()

	try:
		url_date = datetime.strptime(date, "%m%d%y").strftime("%Y-%m-%d")
	except ValueError:
		return redirect(url_for('task.home'))

	prior_date = (datetime.strptime(date, "%m%d%y") - timedelta(days=1)).strftime("%m%d%y")
	next_date = (datetime.strptime(date, "%m%d%y") + timedelta(days=1)).strftime("%m%d%y")

	date_text = date_to_text(date, "%m%d%y")

	date_ts = time.mktime(datetime.strptime(url_date, "%Y-%m-%d").timetuple())
	date_nxt_ts = time.mktime((datetime.strptime(url_date, "%Y-%m-%d") + timedelta(days=1)).timetuple())
	
	tasks = db.execute(
		'SELECT t.id, task_text, t.created_at, t.user_id, t.due_date, t.completed'
		' FROM task t JOIN user u ON t.user_id = u.id'
		' WHERE t.due_date = date(?) AND t.user_id = ?'
		' ORDER by t.created_at ASC', (url_date, g.user['id'],)
	).fetchall()

	subtasks = db.execute(
		'SELECT s.id, subtask_text, s.created_at, s.user_id, s.due_date, s.completed, task_id'
		' FROM subtask s'
		' JOIN user u ON s.user_id = u.id'
		' JOIN task t ON t.id = s.task_id'
		' WHERE u.id = ? AND s.due_date = date(?)', (g.user['id'], url_date,)
	).fetchall()

	return render_template('task/index.html', tasks=tasks, subtasks=subtasks, date=date, date_text=date_text, prior_date=prior_date, next_date=next_date)

@bp.route('/new/<date>', methods=('GET', 'POST'))
@login_required
def new(date):

	due_date = datetime.strptime(date, "%m%d%y").strftime("%Y-%m-%d")

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
				'INSERT INTO task (task_text, user_id, due_date)'
				' VALUES (?, ?, ?)',
				(task_text, g.user['id'], due_date,)
			)
			db.commit()

			return redirect(request.referrer)


def get_task(id, check_user=True):
	task = get_db().execute(
		'SELECT t.id, t.created_at, task_text, t.user_id, t.completed, t.completed_at, t.due_date'
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
		task_text = request.form['edit_task_' + str(task['id'])]
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
			return redirect(request.referrer)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	get_task(id)
	subtasks = get_subtasks(id)

	if request.method == "POST":
		db = get_db()
		db.execute('DELETE FROM task WHERE id = ?', (id,))

		if subtasks is None:
			pass
		else:
			db.execute(
				'DELETE FROM subtask WHERE task_id = ?', (id,)
			)

		db.commit()

		return redirect(request.referrer)

@bp.route('/<int:id>/complete', methods=('POST',))
@login_required
def complete(id):
	task = get_task(id)

	if request.method == "POST":
		db = get_db()
		db.execute(
			'UPDATE task SET completed = 1, completed_at = datetime("now", "localtime")'
			' WHERE id = ?',
			(id,)
		)
		db.commit()
		# return redirect(url_for('task.home'))
		return redirect(request.referrer)

@bp.route('/<int:id>/incomplete', methods=('POST',))
@login_required
def undo(id):
	task = get_task(id)

	if request.method == "POST":
		db = get_db()
		db.execute(
			'UPDATE task SET completed = 0, completed_at = NULL'
			' WHERE id = ?',
			(id,)
		)
		db.commit()
		return redirect(request.referrer)

# Get all subtasks for task x
def get_subtasks(id, check_user=True):
	db = get_db()
	
	subtasks = db.execute(
		'SELECT s.id, subtask_text, s.created_at, s.user_id, s.due_date, s.completed, task_id'
		' FROM subtask s'
		' JOIN user u ON s.user_id = u.id'
		' JOIN task t ON t.id = s.task_id'
		' WHERE u.id = ? AND task_id = ?', (g.user['id'], id,)
	).fetchall()

	return subtasks


# Move/Copy to next day
# Should this be a "copy to next day", "move completely to next day", or, only move open items to next day?
@bp.route('/<date>/<int:id>/move', methods=('POST',))
@login_required
def move_to_next_day(id, date):
	task = get_task(id)
	subtasks = get_subtasks(id)

	if request.method == "POST":
		db = get_db()
		db.execute(
			'UPDATE task SET due_date = date(due_date, "+1 day"), completed = 0, completed_at = NULL'
			' WHERE id = ?', (id,)
		)

		if subtasks is None:
			pass
		else:
			db.execute(
				'UPDATE subtask SET due_date = date(due_date, "+1 day")'
				' WHERE task_id = ?', (id,)
			)
		db.commit()

		return redirect(request.referrer)
		flash('Task moved to next day.')






