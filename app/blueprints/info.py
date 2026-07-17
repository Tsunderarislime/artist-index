from flask import render_template, Blueprint

info_blueprint = Blueprint('info', __name__)

@info_blueprint.route('/about')
def about():
    return render_template('info/about.html', title='About')

@info_blueprint.route('/changelog')
def changelog():
    return render_template('info/changelog.html', title='Changelog')
