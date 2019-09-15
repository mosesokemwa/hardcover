import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from config import Config

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

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

manager = Manager(app)
migrate = Migrate(app, db)


if not os.path.exists('logs'):
    os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/hardcover.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Hardcover startup')

from app import models, routes
