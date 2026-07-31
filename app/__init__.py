from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from json import dumps
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'

login.login_message = "You must be logged in to access this page."
login.login_message_category = "info"

def json_dumps(dict):
    return dumps(dict)

app.jinja_env.globals.update(json_dumps=json_dumps)

try:
    upload_directory = app.config['UPLOAD_DIRECTORY']
    os.makedirs(upload_directory, exist_ok=True)
except Exception as e:
    app.logger.exception(e)

from app import routes, models, load_config
