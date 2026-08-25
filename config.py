import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key-does-not-exist'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    UPLOAD_DIRECTORY = os.environ.get('UPLOAD_DIRECTORY') or \
        os.path.join(basedir, 'upload')
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif', '.webp']
    MAX_UPLOAD_MB = os.environ.get('MAX_UPLOAD_MB') or 1000
    MAINTENANCE = False
