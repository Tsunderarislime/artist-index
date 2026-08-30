from app import app
import app.blueprints as bp
from flask import send_from_directory, render_template, request, abort, flash
from flask_login import current_user

app.register_blueprint(bp.index.index_blueprint)
app.register_blueprint(bp.auth.auth_blueprint)
app.register_blueprint(bp.artist.artist_blueprint)
app.register_blueprint(bp.art.art_blueprint)
app.register_blueprint(bp.admin.admin_blueprint)
app.register_blueprint(bp.info.info_blueprint)
app.register_blueprint(bp.errors.errors_blueprint)

@app.route('/upload/<filename>')
def serve_upload(filename):
    referrer = request.referrer
    if not referrer or not referrer.startswith(request.host_url):
        if not current_user.is_authenticated:
            flash(f'Anonymous access from {referrer} is denied.', 'danger')
            abort(403)

    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

@app.before_request
def is_maintenance():
    if not app.config['MAINTENANCE']:
        return

    if request.path.startswith('/static') or request.path.startswith('/login'):
        return

    if current_user.is_authenticated:
        return

    return abort(503)
