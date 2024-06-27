#!/usr/bin/env bash
# Exit on error
set -o errexit

source venv/Scripts/activate
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate
