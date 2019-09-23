#!/bin/sh

APPLICATION_MODE=config.ProductionConfig
flask db upgrade
gunicorn -b 0.0.0.0:5000 hardcover:application