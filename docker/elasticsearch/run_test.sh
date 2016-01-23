docker run -p 9200:9200 -p 9300:9300 \
       -v /var/container/elasticsearch/data:/usr/share/elasticsearch/data \
       --name estest elasticsearch elasticsearch \
       -Des.network.bind_host=0.0.0.0
