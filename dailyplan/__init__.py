import os
from flask import Flask, render_template
from flask_mail import Mail

mail = Mail()

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY=os.environ.get('SECRET_KEY'),
		DATABASE=os.path.join(app.instance_path, 'dailyplan.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass


	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config["MAIL_USE_SSL"] = True
	app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
	app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
	app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
	mail.init_app(app)

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import task
	app.register_blueprint(task.bp)
	app.add_url_rule('/', endpoint="index")

	from . import subtask
	app.register_blueprint(subtask.bp)

	from . import insights
	app.register_blueprint(insights.bp)

	from . import aux
	app.register_blueprint(aux.bp)

	@app.errorhandler(404)
	def not_found(e):
		return render_template('404.html')

	@app.errorhandler(403)
	def not_found(e):
		return render_template('404.html')	

	return app
