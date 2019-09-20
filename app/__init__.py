import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from config import ProductionConfig, TestingConfig, StagingConfig, DevelopmentConfig
from werkzeug.utils import import_string

from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# ######## Enable this for debugging #########
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# ####### Enable this for debugging #########

application = Flask(__name__)
mode = import_string(os.environ["APPLICATION_MODE"])
application.config.from_object(mode)

db = SQLAlchemy(application)
migrate = Migrate(application, db)
moment = Moment(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'

manager = Manager(application)
migrate = Migrate(application, db)


if not os.path.exists('logs'):
    os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/hardcover.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)

    application.logger.setLevel(logging.INFO)
    application.logger.info('Hardcover startup')

from app import models, routes
