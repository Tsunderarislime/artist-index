from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from json import dumps

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

login.login_message = "You must be logged in to access this page."
login.login_message_category = "info"

def json_dumps(dict):
    return dumps(dict)

app.jinja_env.globals.update(json_dumps=json_dumps)

from app import routes, models, errors, profile_images