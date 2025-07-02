#!/bin/sh

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Starting server..."
# Replace with however you run your app (e.g., daphne, uvicorn, etc.)
python manage.py runserver 0.0.0.0:8080
