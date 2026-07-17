from flask import render_template, Blueprint
from app import db

errors_blueprint = Blueprint('error', __name__)

@errors_blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@errors_blueprint.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
