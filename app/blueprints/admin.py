from flask import render_template, flash, Blueprint, redirect, url_for
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.models import User, Configuration
from app.forms import ChangePasswordForm, ConfigForm

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

@admin_blueprint.route('/controlpanel/config', methods=['GET', 'POST'])
@login_required
def config():
    config = db.session.scalars(
        sa.select(Configuration)
    ).all()
    config_names = [c.name for c in config]
    values = [c.value for c in config]
    d_types = [c.d_type for c in config]
    config_form = ConfigForm()

    if config_form.submit.data and config_form.validate_on_submit():
        name = config_form.config.data.strip()
        value = config_form.value.data.strip()
        success = True

        if name not in config_names:
            config_form.config.errors.append("This config variable does not exist.")
            success = False
        else:
            try:
                if isinstance(app.config[name], bool):
                    updated = bool(value)
                    app.config[name] = updated
                elif isinstance(app.config[name], int):
                    updated = int(value)
                    app.config[name] = int(value)
                elif isinstance(app.config[name], float):
                    updated = float(value)
                    app.config[name] = float(value)
                else:
                    updated = value
                    app.config[name] = value
            except Exception as e:
                config_form.value.errors.append(f"The value you entered was not the correct data type. Expected ({type(app.config[name]).__name__}).")
                success = False

        if success:
            flash(f'Successfully updated the config variable {name} to {updated}', 'success')
            db.session.execute(
                sa.update(Configuration).where(Configuration.name == name).values(value=value)
            )
            db.session.commit()

            return redirect(url_for('admin.config'))
            
    return render_template('admin/config.html', title='Config', config=config_names, values=values, d_types=d_types, config_form=config_form, zip=zip)
