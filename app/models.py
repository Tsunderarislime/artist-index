from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}, with ID {self.id}>'

class Artist(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    searchable_name: so.Mapped[str] = so.mapped_column(sa.String(256))
    social_media_links: so.Mapped[sa.JSON] = so.mapped_column(sa.JSON)

    public: so.Mapped[bool] = so.mapped_column(sa.Boolean)

    art: so.WriteOnlyMapped['Art'] = so.relationship(back_populates='artist', cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f'<Artist {self.name}, with ID {self.id},\nsearchable_name {self.searchable_name}>'

class Art(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    source: so.Mapped[str] = so.mapped_column(sa.String(256))
    link: so.Mapped[str] = so.mapped_column(sa.String(256))
    local: so.Mapped[bool] = so.mapped_column(sa.Boolean)

    artist_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Artist.id, ondelete="cascade"), index=True)

    artist: so.Mapped[Artist] = so.relationship(back_populates='art')

    def __repr__(self):
        return f'<Art with ID {self.id},\nsource {self.source},\nlink {self.link},\nlocal {self.local}>'

class Configuration(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    value: so.Mapped[str] = so.mapped_column(sa.String(256))

    d_type: so.Mapped[str] = so.mapped_column(sa.String(16), default='STRING')

    def __repr__(self):
        return f'<Configuration {self.id}, Name: {self.name}, Value: {self.value}>'
