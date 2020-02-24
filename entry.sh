#!/usr/bin/env sh

python manage.py db upgrade
flask run