#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

apt update
apt upgrade libpango-1.0-0

python manage.py collectstatic --no-input
python manage.py migrate
