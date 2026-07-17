from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.models import Artist
from app.forms import ArtistForm, DeleteForm

artist_blueprint = Blueprint('artist', __name__)

@artist_blueprint.route('/add', methods=['GET', 'POST'])
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

                return redirect(url_for('artist.add'))
            else:
                flash(f"Failed to add {form.name.data} ({form.searchable_name.data}) to the database.", 'danger')

    return render_template('artist/addedit.html', title='Add Artist', form=form)

@artist_blueprint.route('/edit/<name>', methods=['GET', 'POST'])
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

                return redirect(url_for('artist.artist', name=form.name.data.strip()))
            else:
                flash(f"Failed to update {form.name.data} ({form.searchable_name.data}) in the database.", 'danger')
    
    return render_template('artist/addedit.html', title=f'Edit {name}', form=form)

@artist_blueprint.route('/artist/<name>', methods=['GET', 'POST'])
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

            return redirect(url_for('index.index'))
        else:
            return render_template('artist/artist.html', title=name, artist=artist, form=form, hide_modal='ThisEvaluatesToTrueInJavaScript')

    return render_template('artist/artist.html', title=name, artist=artist, form=form, hide_modal='')
