#!/bin/bash

#./initDocker.sh
cd ~/Pinbot/
source pin_venv/bin/activate
python manage.py migrate
#python manage.py runserver 192.168.199.114:8000
python manage.py runserver 0.0.0.0:8000
#python manage.py runserver 127.0.0.1:8000
