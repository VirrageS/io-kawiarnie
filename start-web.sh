#!/bin/sh

cd caffe;
sleep 5;
su -m docker -c "python3 manage.py migrate"
# su -m docker -c "python3 manage.py runserver 0.0.0.0:8000"
su -m docker -c "gunicorn caffe.wsgi:application -w 4 -b :8000"
