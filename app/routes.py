from app import app
import app.blueprints as bp

app.register_blueprint(bp.index.index_blueprint)
app.register_blueprint(bp.auth.auth_blueprint)
app.register_blueprint(bp.artist.artist_blueprint)
app.register_blueprint(bp.admin.admin_blueprint)
app.register_blueprint(bp.info.info_blueprint)
app.register_blueprint(bp.errors.errors_blueprint)
