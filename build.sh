#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure the virtual environment is activated
source /opt/render/project/src/venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate
