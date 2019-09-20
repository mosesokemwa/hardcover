#!/bin/sh

# APPLICATION_MODE=config.ProductionConfig
APPLICATION_MODE=config.DevelopmentConfig
flask db upgrade
gunicorn hardcover:application