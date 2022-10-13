#!/bin/bash

python manage.py migrate
python update_products.py

python manage.py runserver 0.0.0.0:8080