DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS subtask;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(128) NOT NULL,
	email VARCHAR(128) UNIQUE NOT NULL,
	password VARCHAR(128) NOT NULL,
	created_at TIMESTAMP DEFAULT (datetime('now','localtime')),
	last_login TIMESTAMP DEFAULT (datetime('now','localtime')),
	timezone VARCHAR(40),
	dark_mode BOOLEAN DEFAUlT 0,
	week_view BOOLEAN DEFAULT 0
);

CREATE TABLE task (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
	task_text VARCHAR(128) NOT NULL,
	completed BOOLEAN NOT NULL DEFAULT 0,
	completed_at TIMESTAMP,
	due_date TEXT NOT NULL DEFAULT (date('now','localtime')),
	FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE subtask (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	task_id INTEGER NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
	subtask_text VARCHAR(128) NOT NULL,
	completed BOOLEAN NOT NULL DEFAULT 0,
	completed_at TIMESTAMP,
	due_date TEXT NOT NULL DEFAULT (date('now','localtime')),
	FOREIGN KEY (user_id) REFERENCES user (id),
	FOREIGN KEY (task_id) REFERENCES task (id)
);