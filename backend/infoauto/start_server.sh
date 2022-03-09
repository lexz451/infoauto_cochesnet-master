#!/bin/bash
export CELERY_BROKER_URL='localhost:6379'
#export DATABASE_URL='mysql://localhost:3306'
python manage.py runserver 0.0.0.0:8000 --insecure
