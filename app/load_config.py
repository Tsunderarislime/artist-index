from app import app, db
import sqlalchemy as sa
from app.models import Configuration

with app.app_context():
    try:
        maintenance = db.session.scalars(
            sa.select(Configuration).where(Configuration.name == 'MAINTENANCE')
        ).first()
        allowed_referrer_url = db.session.scalars(
            sa.select(Configuration).where(Configuration.name == 'ALLOWED_REFERRER_URL')
        ).first()

        if not maintenance:
            app.logger.info('No MAINTENANCE config found in database. Creating an entry for MAINTENANCE.')
            m = Configuration(name='MAINTENANCE', value='', d_type='BOOLEAN')
            db.session.add(m)
            db.session.commit()
            app.config['MAINTENANCE'] = False
        else:
            app.config['MAINTENANCE'] = bool(maintenance.value)

        if not allowed_referrer_url:
            app.logger.info('No ALLOWED_REFERRER_URL config found in database. Creating an entry for ALLOWED_REFERRER_URL.')
            aru = Configuration(name='ALLOWED_REFERRER_URL', value='http://localhost:8000', d_type='STRING')
            db.session.add(aru)
            db.session.commit()
            app.config['ALLOWED_REFERRER_URL'] = 'http://localhost:8000'
        else:
            app.config['ALLOWED_REFERRER_URL'] = allowed_referrer_url.value

    except Exception as e:
        app.logger.exception(e)
