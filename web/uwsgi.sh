#!/bin/env bash
ELECPROGWEB_PATH=.
source $ELECPROGWEB_PATH/env/bin/activate
uwsgi --chdir=$ELECPROGWEB_PATH \
    --module=elecprog.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=elecprog.settings \
    --master --pidfile=/tmp/project-master.pid \
    --socket=0.0.0.0:8001 \
    --processes=5 \
    --harakiri=20 \
    --max-requests=5000 \
    --uid=1000 --gid=2000 \
    --vacuum \
    --home=$ELECPROGWEB_PATH/env \
    --daemonize=/tmp/elecprogweb.log
