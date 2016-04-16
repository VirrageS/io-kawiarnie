#!/bin/sh

cd caffe;
sleep 5;
su -m docker -c "python3 manage.py migrate"
su -m docker -c "python3 manage.py runserver 0.0.0.0:8000"

# uwsgi --http :8000 --module caffe.wsgi
