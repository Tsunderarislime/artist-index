from flask import render_template, flash, Blueprint
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User
from app.forms import ChangePasswordForm

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/controlpanel', methods=['GET', 'POST'])
@login_required
def controlpanel():
    change_password_form = ChangePasswordForm()

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

    return render_template('admin/controlpanel.html', title='Control Panel', change_password_form=change_password_form)
