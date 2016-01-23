#!/usr/bin/env bash
# prepare the context
rm -rf build/
mkdir build/
cp ../../web/requirements.txt build/ -r
cp ../../web/elecprog build/ -r
cp ../../web/appelec build/ -r
cp ../../web/manage.py build/ -r
cp ../../web/uwsgi.ini build/ -r
# build docker image
sudo docker build -t funeslab/uwsgielec:v0 .
