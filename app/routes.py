from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.models import User, Artist
from app.forms import LoginForm, ArtistForm, DeleteForm

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        artists = db.session.scalars(
            sa.select(Artist)
        ).all()
        return render_template('index.html', title='Home', artists=artists)
    else:
        artists = db.session.scalars(
            sa.select(Artist).where(Artist.public == True)
        ).all()
        return render_template('index.html', title='Home', artists=artists)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ArtistForm()

    if form.validate_on_submit():
        links = {}
        successes = 0
        for link in form.social_media_links.data:
            if link['social_media'].strip() and link['link'].strip():
                links[link['social_media'].strip()] = link['link'].strip()
                successes += 1
            else:
                flash(f"Failed to add social media link: \"{link['social_media']}\" ({link['link']}).", 'warning')

        if successes > 0:
            flash(f"Successfully added {form.name.data} ({form.searchable_name.data}) to the database.", 'success')
            artist = Artist(name=form.name.data.strip(), searchable_name=form.searchable_name.data.strip(), public=form.public.data, social_media_links=links)
            db.session.add(artist)
            db.session.commit()
        else:
            flash(f"Failed to add {form.name.data} ({form.searchable_name.data}) to the database.", 'danger')

        return redirect(url_for('add'))
    
    return render_template('add.html', title='Add Artist', form=form)

@app.route('/artist/<name>', methods=['GET', 'POST'])
def artist(name):
    artist = db.first_or_404(sa.select(Artist).where(Artist.name == name))
    form = DeleteForm()

    if current_user.is_authenticated and form.validate_on_submit():
        success = True

        if form.name.data.strip() != name:
            form.name.errors.append("The names did not match, please try again.")
            success = False
        
        if not form.double_check.data:
            form.double_check.errors.append("Please check the box to confirm.")
            success = False
        
        if success:
            flash(f'Successfully deleted {name} from the database.', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('artist.html', artist=artist, form=form, hide_modal='ThisEvaluatesToTrueInJavaScript')

    return render_template('artist.html', artist=artist, form=form, hide_modal='')

@app.route('/about')
def about():
    return render_template('about.html', title='About')