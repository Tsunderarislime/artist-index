from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError
import sqlalchemy as sa
from app import db
from app.models import Artist

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SocialForm(FlaskForm):
    class Meta:
        csrf = False
    
    social_media = StringField('Social Media')
    link = StringField('Link')

class ArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    searchable_name = StringField('Searchable Name')
    social_media_links = FieldList(FormField(SocialForm), min_entries=1)
    public = BooleanField('Public')
    submit = SubmitField('Submit')

    def validate_name(self, name):
        artist = db.session.scalar(sa.select(Artist).where(
            Artist.name == name.data
        ))

        if artist is not None:
            raise ValidationError('Artist already exists in database.')

class DeleteForm(FlaskForm):
    class Meta:
        csrf = False
    
    name = StringField('Name')
    double_check = BooleanField('Double Check')
    submit = SubmitField('Delete')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    change_password_submit = SubmitField('Change Password')

class FetchButtonForm(FlaskForm):
    class Meta:
        csrf = False
    
    fetch_button_submit = SubmitField('Fetch')