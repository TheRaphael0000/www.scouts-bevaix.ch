#!/bin/bash

python manage.py collectstatic --no-input

python -m gunicorn --bind "0.0.0.0:80" scoutsbevaix.wsgi:application