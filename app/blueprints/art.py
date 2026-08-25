from flask import render_template, Blueprint
from flask_login import current_user
import sqlalchemy as sa
from app import db
from app.models import Artist, Art

art_blueprint = Blueprint('art', __name__)

@art_blueprint.route('/browse')
def browse():
    if current_user.is_authenticated:
        artist_ids = db.session.scalars(
            sa.select(Artist.id)
        ).all()
    else:
        artist_ids = db.session.scalars(
            sa.select(Artist.id).where(Artist.public == True)
        ).all()

    art = db.session.scalars(
        sa.select(Art).where(Art.artist_id.in_(artist_ids))
    ).all()

    return render_template('art/browse.html', title='Browse Art', art=art)
