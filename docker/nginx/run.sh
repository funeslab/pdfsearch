#!/usr/bin/env bash
if [ -z "$1" ]
then
    daemon="-d --log-driver=fluentd --restart=always"
else
    daemon=""
fi
docker run --name nginx \
       $daemon \
       --link elecprogweb \
       --link cosweb \
       -p 80:80 \
       funeslab/nginx-cos-elec:v0
