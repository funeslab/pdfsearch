#!/usr/bin/env bash
if [ -z "$1" ]
then
    daemon="-d --log-driver=fluentd --restart=always"
else
    daemon=""
fi
sudo docker run  --name elecprogweb \
       $daemon \
       --link elasticsearch \
       -e "SECRET_KEY=ASPP23J32LKJK" \
       funeslab/uwsgielec:v0
