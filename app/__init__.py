import os
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
from app.models import User

from app import routes
print(os.environ['APP_SETTINGS'])
