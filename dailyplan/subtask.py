from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from dailyplan.auth import login_required, get_user
from dailyplan.db import get_db
from dailyplan.date import date_to_text, add_suffix

from datetime import date, datetime, timedelta
import time
import re

bp = Blueprint('subtask', __name__, url_prefix='/subtask')

def get_subtask(id):
	subtask = get_db().execute(
		'SELECT *'
		' FROM subtask s'
		' JOIN user u ON s.user_id = u.id'
		' WHERE u.id = ? AND s.id = ?', (g.user['id'], id,)
	).fetchone()

	if subtask is None:
		abort(404, "Subtask id {id} doesn't exist.")

	return subtask

@bp.route('/<date>/<int:task_id>', methods=('GET', 'POST'))
@login_required
def new(date, task_id):

	due_date = datetime.strptime(date, "%m%d%y").strftime("%Y-%m-%d")

	if request.method == 'POST':
		subtask_text = request.form['subtask_text_' + str(task_id)]
		error = None

		if not subtask_text:
			error = "Subtask action is required."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO subtask (subtask_text, task_id, user_id, due_date)'
				' VALUES (?, ?, ?, ?)',
				(subtask_text, task_id, g.user['id'], due_date,)
			)
			db.commit()

			return redirect(url_for('task.index', date=date))


# Delete Subtask
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	get_subtask(id)
	db = get_db()
	db.execute('DELETE FROM subtask WHERE id = ?', (id,))
	db.commit()

	return redirect(request.referrer)

# Complete Subtask
@bp.route('/<int:id>/complete', methods=('POST',))
@login_required
def complete(id):
	get_subtask(id)
	db = get_db()
	db.execute('UPDATE subtask SET completed = 1, completed_at = ? WHERE id = ?', (datetime.now(), id,))
	db.commit()

	return redirect(request.referrer)

# Un-complete Subtask
@bp.route('/<int:id>/incomplete', methods=('POST',))
@login_required
def undo(id):
	subtask = get_subtask(id)

	if request.method == "POST":
		db = get_db()
		db.execute(
			'UPDATE subtask SET completed = 0, completed_at = NULL'
			' WHERE id = ?',
			(id,)
		)
		db.commit()
		return redirect(request.referrer)


# Edit subtask?

