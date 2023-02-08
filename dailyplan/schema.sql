DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS subtask;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(40) NOT NULL,
	email VARCHAR(120) UNIQUE NOT NULL,
	password VARCHAR(128) NOT NULL,
	date_created TIMESTAMP DEFAULT (datetime('now','localtime')),
	last_login TIMESTAMP,
	timezone VARCHAR(40),
	dark_mode BOOLEAN DEFAUlT 0,
	week_view BOOLEAN DEFAULT 0

);

CREATE TABLE task (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
	task_text VARCHAR(128) NOT NULL,
	completed BOOLEAN NOT NULL DEFAULT 0,
	due_date TEXT NOT NULL DEFAULT (date('now','localtime')),
	FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE subtask (
	id integer PRIMARY KEY AUTOINCREMENT,
	created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
	task_text VARCHAR(128) NOT NULL,
	completed BOOLEAN NOT NULL DEFAULT 0,
	due_date TIMESTAMP NOT NULL DEFAULT (date('now','localtime')),
	FOREIGN KEY (task_id) REFERENCES task (id)
);