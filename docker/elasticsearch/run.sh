#!/usr/bin/env bash
if [ -z "$1" ]
then
    daemon="-d --log-driver=fluentd --restart=always"
else
    daemon=""
fi
# fluentd link is for order not for need a true link
docker run  --name elasticsearch \
       $daemon \
       --link fluentd \
       -v /var/container/elasticsearch/data:/usr/share/elasticsearch/data \
       elasticsearch \
       -Des.network.bind_host=0.0.0.0
