import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_TITLE = 'Book Store'

class Config(object):
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(PROJECT_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@localhost:15432/hardcover
