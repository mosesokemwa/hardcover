#!/bin/sh

APPLICATION_MODE=config.ProductionConfig
flask db upgrade
gunicorn hardcover:application