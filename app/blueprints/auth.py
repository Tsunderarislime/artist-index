from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import db
from app.models import User
from app.forms import LoginForm

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        
        next_page = request.args.get('next')

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login', next=next_page))

        login_user(user, remember=form.remember_me.data)

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
