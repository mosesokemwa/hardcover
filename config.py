import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_TITLE = 'Book Store'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(PROJECT_DIR, 'app.db')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    FLASK_ENV = "development"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@localhost/hardcover'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(PROJECT_DIR, '/app/tests/test.db')
