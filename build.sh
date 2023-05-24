#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
pip3 install requirements.txt
python baseapp/manage.py collectstatic --no-input
python baseapp/manage.py migrate