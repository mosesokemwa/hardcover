#!/bin/sh

flask db upgrade
flask run -h 0.0.0.0 -p 5000