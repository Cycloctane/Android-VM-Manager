#! /bin/bash

celery -A app.celery_app worker -l info -E