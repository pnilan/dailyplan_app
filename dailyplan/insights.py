from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from werkzeug.exceptions import abort

from dailyplan.auth import login_required, get_user
from dailyplan.db import get_db

from datetime import date, datetime, timedelta
import numpy as np

bp = Blueprint('insights', __name__)

# Return count of tasks created by user
def total_tasks_created():
	db = get_db()
	user = get_user(g.user['id'])

	tasks = db.execute(
		'SELECT count(*) as total'
		' FROM task t JOIN user u ON t.user_id = u.id'
		' WHERE t.user_id = ?', (user['id'],)
	).fetchone()
	return tasks['total']

# Return count of tasks completed by user
def total_tasks_completed():
	db = get_db()
	user = get_user(g.user['id'])

	completed_tasks = db.execute(
		'SELECT count(*) as total'
		' FROM task t JOIN user u ON t.user_id = u.id'
		' WHERE t.user_id = ? AND t.completed = 1', (user['id'],)
	).fetchone()
	return completed_tasks['total']

# Return count of substasks created by user
def total_subtasks_created():
	db = get_db()
	user = get_user(g.user['id'])

	subtasks = db.execute(
		'SELECT count(*) as total'
		' FROM subtask s'
		' JOIN user u ON s.user_id = u.id'
		' WHERE u.id = ?', (user['id'],)
	).fetchone()
	return subtasks['total']

# Return count of subtasks completed by user
def total_subtasks_completed():
	db = get_db()
	user = get_user(g.user['id'])

	completed_subtasks = db.execute(
		'SELECT count(*) as total'
		' FROM subtask s'
		' JOIN user u ON s.user_id = u.id'
		' WHERE u.id = ? AND s.completed = 1', (user['id'],)
	).fetchone()
	return completed_subtasks['total']

# Determine average time taken to complete a task
def task_time_completion():
	db = get_db()
	user = get_user(g.user['id'])

	tasks = db.execute(
		'SELECT t.id, t.user_id, t.created_at, t.completed, t.completed_at'
		' FROM task t'
		' JOIN user u ON t.user_id = u.id'
		' WHERE t.user_id = ? AND completed = 1', (user['id'],)
	).fetchall()

	t_array = []

	for t in tasks:
		created_at = int(t['created_at'].strftime('%s'))
		completed_at = int(t['completed_at'].strftime('%s'))
		t_array.append(completed_at - created_at)

	if len(t_array) == 0:
		return "N/A", "N/A", "", ""
	else:
		average_time_seconds = round(np.average(t_array), 1)
		median_time_seconds = round(np.median(t_array), 1)

		if average_time_seconds < 86400:
			average_time_hours = str(round(average_time_seconds / 3600, 1))
			median_time_hours = str(round(median_time_seconds / 3600, 1))

			if average_time_hours == 1:
				avg_time_unit = "hour"
			else:
				avg_time_unit = "hours"

			if median_time_hours == 1:
				med_time_unit = "hour"
			else:
				med_time_unit = "hours"

			return average_time_hours, median_time_hours, avg_time_unit, med_time_unit

		else:
			average_time_days = str(round(average_time_seconds / 86400, 1))
			median_time_days = str(round(median_time_seconds / 86400, 1))

			if average_time_days == 1:
				avg_time_unit = "day"
			else:
				avg_time_unit = "days"

			if median_time_days == 1:
				med_time_unit = "day"
			else:
				med_time_unit = "days"

			return average_time_days, median_time_days, avg_time_unit, med_time_unit



@bp.route('/insights')
@login_required
def insights():
	user = get_user(g.user['id'])

	tasks_created = total_tasks_created()
	tasks_completed = total_tasks_completed()
	subtasks_created = total_subtasks_created()
	subtasks_completed = total_subtasks_completed()
	sum_tasks = tasks_created + subtasks_created
	sum_tasks_completed = tasks_completed + subtasks_completed
	average_time, median_time, avg_time_unit, med_time_unit = task_time_completion()


	return render_template('insights/insights.html', user=user, tasks_created=tasks_created, tasks_completed=tasks_completed, subtasks_created=subtasks_created, subtasks_completed=subtasks_completed, sum_tasks=sum_tasks, sum_tasks_completed=sum_tasks_completed, average_time=average_time, median_time=median_time, avg_time_unit=avg_time_unit, med_time_unit=med_time_unit)