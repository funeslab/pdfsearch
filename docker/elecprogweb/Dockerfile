FROM debian:jessie
# MAINTAINER ddorado

RUN apt-get update \
        && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
                build-essential \
		libpcre3 \
		libpcre3-dev \
                python \
                python-dev \
                libpq-dev \
                python-pip \
        && rm -fr /var/lib/apt/lists/* \
        && rm -fr /tmp/* \
        && rm -fr /var/tmp/*

# Set up package and requirements
# RUN mkdir -p /opt/django
COPY build/requirements.txt /tmp/
RUN cd /tmp/ && pip install -r requirements.txt
ADD build/elecprog/ /opt/django/elecprogweb/elecprog/
ADD build/appelec/ /opt/django/elecprogweb/appelec/
ADD build/manage.py /opt/django/elecprogweb/
ADD build/uwsgi.ini /etc/

EXPOSE 8080 9191
CMD ["/usr/local/bin/uwsgi", "/etc/uwsgi.ini"]