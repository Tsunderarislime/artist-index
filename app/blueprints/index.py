from flask import render_template, Blueprint
from flask_login import current_user
import sqlalchemy as sa
from app import db
from app.models import Artist

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
@index_blueprint.route('/index')
def index():
    if current_user.is_authenticated:
        artists = db.session.scalars(
            sa.select(Artist)
        ).all()

        return render_template('index/index.html', title='Home', artists=artists)
    else:
        artists = db.session.scalars(
            sa.select(Artist).where(Artist.public == True)
        ).all()

        return render_template('index/index.html', title='Home', artists=artists)
    