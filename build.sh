#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

sudo apt-get update
sudo apt-get upgrade libpango-1.0-0

python manage.py collectstatic --no-input
python manage.py migrate
