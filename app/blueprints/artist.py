from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.models import Artist, Art
from app.forms import ArtistForm, DeleteForm, ArtUploadForm, ArtEditForm
from werkzeug.utils import secure_filename
import hashlib
import os

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

    return render_template('artist/addeditartist.html', title='Add Artist', form=form)

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
    
    return render_template('artist/addeditartist.html', title=f'Edit {name}', form=form)

@artist_blueprint.route('/artist/<name>', methods=['GET', 'POST'])
def artist(name):
    artist = db.first_or_404(sa.select(Artist).where(Artist.name == name))
    art = db.session.scalars(
        sa.select(Art).where(Art.artist_id == artist.id)
    ).all()
    delete_form = DeleteForm()
    art_upload_form = ArtUploadForm()

    # This prevents anonymous users from deleting an artist even if they somehow gain access to the deletion form
    if current_user.is_authenticated and delete_form.submit.data and delete_form.validate_on_submit():
        success = True

        if delete_form.name.data.strip() != name:
            delete_form.name.errors.append("The names did not match, please try again.")
            success = False

        if not delete_form.double_check.data:
            delete_form.double_check.errors.append("Please check the box to confirm.")
            success = False

        if success:
            flash(f'Successfully deleted {name} from the database. All of their art has also been deleted from the database.', 'success')

            for a in art:
                if a.local:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_DIRECTORY'], a.link))
                    except OSError:
                        pass

            db.session.delete(artist)
            db.session.execute(
                sa.delete(Art).where(Art.artist_id == artist.id)
            )
            db.session.commit()

            return redirect(url_for('index.index'))
        else:
            return render_template('artist/artist.html', title=name, artist=artist, art=art,
                                   delete_form=delete_form, art_upload_form=art_upload_form, 
                                   hide_delete_modal='ThisEvaluatesToTrueInJavaScript', hide_art_upload_modal='')


    if current_user.is_authenticated and art_upload_form.art_upload_submit.data and art_upload_form.validate_on_submit():
        success = True

        if not art_upload_form.source.data:
            art_upload_form.source.errors.append("Please provide a source for the image.")
            success = False

        # Add a success check here to skip file processing if they upload a file with no source
        if success and art_upload_form.file.data:
            file = art_upload_form.file.data
            filename = secure_filename(file.filename)

            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    art_upload_form.file.errors.append("Please upload a JPG, PNG, GIF, or WEBP.")
                    success = False

                else:
                    saved_filename = os.path.join(app.config['UPLOAD_DIRECTORY'], filename)
                    file.save(saved_filename)

                    with open(saved_filename, 'rb') as f:
                        h = hashlib.shake_256(f.read())
                        renamed = f'{h.hexdigest(32)}{file_ext}'
                        target = os.path.join(app.config['UPLOAD_DIRECTORY'], renamed)

                        if os.path.isfile(target):
                            success = False
                            art_upload_form.file.errors.append("The file you upload already exists in the database.")
                            os.remove(saved_filename)

                        else:
                            os.replace(saved_filename, target)

                        f.close()

                        link = renamed
                        local = True
                        success_message = 'Successfully uploaded the image to the database.'
                    
            else:
                art_upload_form.file.errors.append("Please upload an image.")
                success = False

        elif art_upload_form.link.data:
            link = art_upload_form.link.data
            local = False
            success_message = 'Successfully add the image link.'

        elif success:
            success = False
            art_upload_form.file.errors.append("Please upload an image or provide a link to an image.")

        if success:
            flash(success_message, 'success')
            a = Art(source=art_upload_form.source.data.strip(), link=link.strip(), local=local, artist=artist)
            db.session.add(a)
            db.session.commit()

            return redirect(url_for('artist.artist', name=artist.name))

        else:
            return render_template('artist/artist.html', title=name, artist=artist, art=art,
                                   delete_form=delete_form, art_upload_form=art_upload_form, 
                                   hide_delete_modal='', hide_art_upload_modal='ThisEvaluatesToTrueInJavaScript')


    return render_template('artist/artist.html', title=name, artist=artist, art=art,
                           delete_form=delete_form, art_upload_form=art_upload_form, 
                           hide_delete_modal='', hide_art_upload_modal='')

@artist_blueprint.route('/artist/<name>/editart', methods=['GET', 'POST'])
@login_required
def editart(name):
    artist = db.first_or_404(sa.select(Artist).where(Artist.name == name))
    art = db.session.scalars(
        sa.select(Art).where(Art.artist_id == artist.id)
    ).all()
    form = ArtEditForm(
        art=[{'link': a.link, 'source': a.source, 'delete': False} for a in art],
    )

    if form.validate_on_submit():
        delete_ids = []
        deletion_count = 0
        for a, a_form in zip(art, form.art):
            if a_form.delete.data:
                delete_ids.append(a.id)
                deletion_count += 1
                if a.local:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_DIRECTORY'], a.link))
                    except OSError:
                        pass
            else:
                db.session.execute(
                    sa.update(Art).where(Art.id == a.id).values(
                        source=a_form.source.data.strip(),
                        link=a_form.link.data.strip()
                    )
                )

        db.session.execute(
            sa.delete(Art).where(Art.id.in_(delete_ids))
        )
        db.session.commit()

        flash(f'Successfully updated art in the database for {artist.name}.', 'success')
        if deletion_count:
            flash(f'Deleted {deletion_count} artwork(s) from the database.', 'info')

        return redirect(url_for('artist.editart', name=artist.name))

    return render_template('artist/editart.html', title=name, artist=artist, art=art, form=form, zip=zip)
