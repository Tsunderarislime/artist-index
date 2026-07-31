from app import app, db
import sqlalchemy as sa
from app.models import Configuration

with app.app_context():
    try:
        maintenance = db.session.scalars(
            sa.select(Configuration).where(Configuration.name == 'MAINTENANCE')
        ).first()

        if not maintenance:
            app.logger.info('No MAINTENANCE config found in database. Creating an entry for MAINTENANCE.')
            m = Configuration(name='MAINTENANCE', value='', d_type='BOOLEAN')
            db.session.add(m)
            db.session.commit()
            app.config['MAINTENANCE'] = False
        else:
            app.config['MAINTENANCE'] = bool(maintenance.value)

    except Exception as e:
        app.logger.exception(e)
