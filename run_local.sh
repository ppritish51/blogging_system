#!/bin/bash

# Step 1: Activate the virtual environment
source ./venv/bin/activate

# Step 2: Print the path of the activated virtual environment
echo "Activated virtual environment at $VIRTUAL_ENV"

# Step 3: Export the settings module environment variable
export DJANGO_SETTINGS_MODULE=CheetahMatrix.settings.local

# Step 4: Create the database migrations
python manage.py makemigrations

# Step 5: Apply the database migrations
python manage.py migrate

# python manage.py collectstatic
# python manage.py createsuperuser

# Step 6: Start the Django development server
python manage.py runserver
