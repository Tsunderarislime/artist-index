from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.models import User, Artist
from app.forms import LoginForm, ArtistForm, DeleteForm, ChangePasswordForm, FetchButtonForm
from app.profile_images import fetch_profile_images

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/')
@app.route('/index')
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
        check_existing = db.session.scalar(sa.select(Artist).where(
            Artist.name == form.name.data.strip()
        ))

        if check_existing is not None:
            flash(f"Failed to add {form.name.data} ({form.searchable_name.data}) to the database.", 'danger')
            form.name.errors.append("This artist already exists in the database.")
        else:
            links = {}
            successes = 0
            for link in form.social_media_links.data:
                if link['social_media'].strip() and link['link'].strip():
                    links[link['social_media'].strip()] = link['link'].strip()
                    successes += 1
                else:
                    flash(f"Failed to add social media link: \"{link['social_media']}\" ({link['link']}).", 'warning')

            if successes:
                flash(f"Successfully added {form.name.data} ({form.searchable_name.data}) to the database.", 'success')
                artist = Artist(name=form.name.data.strip(), searchable_name=form.searchable_name.data.strip(), public=form.public.data, social_media_links=links)
                db.session.add(artist)
                db.session.commit()

                return redirect(url_for('index'))
            else:
                flash(f"Failed to add {form.name.data} ({form.searchable_name.data}) to the database.", 'danger')

    return render_template('addedit.html', title='Add Artist', form=form)

@app.route('/artist/<name>', methods=['GET', 'POST'])
def artist(name):
    artist = db.first_or_404(sa.select(Artist).where(Artist.name == name))
    form = DeleteForm()

    # This prevents anonymous users from deleting an artist even if they somehow gain access to the deletion form
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
            db.session.delete(artist)
            db.session.commit()

            return redirect(url_for('index'))
        else:
            return render_template('artist.html', title=name, artist=artist, form=form, hide_modal='ThisEvaluatesToTrueInJavaScript')

    return render_template('artist.html', title=name, artist=artist, form=form, hide_modal='')

@app.route('/edit/<name>', methods=['GET', 'POST'])
@login_required
def edit(name):
    artist = db.first_or_404(sa.select(Artist).where(Artist.name == name))
    form = ArtistForm(
        name=artist.name,
        searchable_name=artist.searchable_name,
        social_media_links=[{'social_media': social_media, 'link': link} for social_media, link in artist.social_media_links.items()],
        public=artist.public
    )

    if form.validate_on_submit():
        check_existing = db.session.scalar(sa.select(Artist).where(
            Artist.name == form.name.data.strip()
        ))

        # This makes sure you can't edit the current artist's name into another existing artist's name
        if not form.name.data.strip() == name and check_existing is not None:
            flash(f"Failed to update {name} ({artist.searchable_name}) in the database.", 'danger')
            form.name.errors.append("This artist already exists in the database.")
        else:
            links = {}
            successes = 0
            for link in form.social_media_links.data:
                if link['social_media'].strip() and link['link'].strip():
                    links[link['social_media'].strip()] = link['link'].strip()
                    successes += 1
                else:
                    flash(f"Failed to add social media link: \"{link['social_media']}\" ({link['link']}).", 'warning')

            if successes:
                flash(f"Successfully updated {form.name.data} ({form.searchable_name.data}) in the database.", 'success')
                db.session.execute(
                    sa.update(Artist).where(Artist.name == name).values(
                        name=form.name.data.strip(),
                        searchable_name=form.searchable_name.data.strip(),
                        public=form.public.data,
                        social_media_links=links
                    )
                )
                db.session.commit()

                return redirect(url_for('artist', name=form.name.data.strip()))
            else:
                flash(f"Failed to update {form.name.data} ({form.searchable_name.data}) in the database.", 'danger')
    
    return render_template('addedit.html', title=f'Edit {name}', form=form)

@app.route('/controlpanel', methods=['GET', 'POST'])
@login_required
def controlpanel():
    change_password_form = ChangePasswordForm()
    fetch_button_form = FetchButtonForm()

    if change_password_form.change_password_submit.data and change_password_form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == current_user.username))
        
        if not user.check_password(change_password_form.current_password.data):
            change_password_form.current_password.errors.append("Incorrect password")
        elif len(change_password_form.new_password.data) < 8:
            change_password_form.new_password.errors.append("Password too short. It should be at least 8 characters long.")
        else:
            flash('Successfully updated your password.', 'success')
            user.set_password(change_password_form.new_password.data)
            db.session.commit()
    
    if fetch_button_form.fetch_button_submit.data and fetch_button_form.validate_on_submit():
        if fetch_profile_images():
            flash('Successfully fetched profile images', 'success')
        else:
            flash('Failed to fetch profile images.', 'danger')

    return render_template('controlpanel.html', title='Control Panel', change_password_form=change_password_form, fetch_button_form=fetch_button_form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')