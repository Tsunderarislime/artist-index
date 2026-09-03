from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SocialField(FlaskForm):
    class Meta:
        csrf = False

    social_media = StringField('Social Media')
    link = StringField('Link')

class ArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    searchable_name = StringField('Searchable Name')
    social_media_links = FieldList(FormField(SocialField), min_entries=1)
    public = BooleanField('Public')
    submit = SubmitField('Submit')

class ArtUploadForm(FlaskForm):
    file = FileField('File')
    link = StringField('Link')
    source = StringField('Source')
    art_upload_submit = SubmitField('Upload')

class ArtEditField(FlaskForm):
    class Meta:
        csrf = False

    link = StringField('Link')
    source = StringField('Source')
    delete = BooleanField('Delete')

class ArtEditForm(FlaskForm):
    art = FieldList(FormField(ArtEditField))
    submit = SubmitField('Save changes')

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

class ConfigForm(FlaskForm):
    config = StringField('Config', validators=[DataRequired()])
    value = StringField('Value')
    submit = SubmitField('Set Config')

class ManageStorageForm(FlaskForm):
    class Meta:
        csrf = False

    ids = StringField('IDs')
    double_check = BooleanField('Double Check')
    submit = SubmitField('Delete')
