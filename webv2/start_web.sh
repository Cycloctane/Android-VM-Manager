#! /bin/bash

uvicorn --factory app:create_app --host=$app_host --port=$app_port