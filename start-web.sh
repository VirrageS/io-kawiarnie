#!/bin/sh

cd caffe
su -m docker -c "python3 manage.py migrate"
su -m docker -c "python3 manage.py runserver 0.0.0.0:8000"
