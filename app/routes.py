from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f'User: {form.username.data} logged in. Remember Me: {form.remember_me.data}.')
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')