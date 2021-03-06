import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = 'danger'

if not app.debug:
	if app.config['MAIL_SERVER']:
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
						fromaddr='no-reply@'+app.config['MAIL_SERVER'],
						toaddrs= app.config['ADMINS'], subject="App Failure",
						credentials=auth, secure=secure)
		print('Throwing Error')
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)
		# if not os.path.exists('logs'):
		# 	os.mkdir('logs')
		# file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
		# 				 backupCount=10)
		# file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
		# file_handler.setLevel(logging.INFO)
		# app.logger.addHandler(file_handler)

		# app.logger.setLevel(logging.INFO)
		# app.logger.info('App Startup')

from app.models import User
from app import routes, errors






print(os.environ['APP_SETTINGS'])
