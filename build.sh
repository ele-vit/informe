#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
apt-get install -y py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango
python manage.py collectstatic --no-input
python manage.py migrate
