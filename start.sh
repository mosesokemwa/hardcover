#!/bin/sh

export APPLICATION_MODE=config.ProductionConfig
flask db upgrade
# gunicorn -b 0.0.0.0:5000 hardcover:application
flask run -h 0.0.0.0 -p 5000