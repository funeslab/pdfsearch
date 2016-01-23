FROM nginx
EXPOSE 80
# Override default
COPY build/cosweb /var/cosweb/
COPY build/cosapp_nginx.conf /etc/nginx/conf.d/
COPY build/elecprogweb /var/elecprogweb/
COPY build/elecprog_nginx.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf
