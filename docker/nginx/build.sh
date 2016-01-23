rm -rf build
# prepare the context
mkdir -p build/elecprogweb/appelec
cp ../../web/elecprog_nginx.conf build
cp ../../web/uwsgi_params build/elecprogweb
cp ../../web/appelec/static build/elecprogweb/appelec -r
# yui-compressor
DIR=build/elecprogweb/appelec/static/appelec
yui-compressor $DIR/programs.js -o /tmp/tmp.js
cp /tmp/tmp.js $DIR/programs.js
yui-compressor $DIR/search.js -o /tmp/tmp.js
cp /tmp/tmp.js $DIR/search.js
yui-compressor $DIR/js/common.js -o /tmp/tmp.js
cp /tmp/tmp.js $DIR/js/common.js
yui-compressor $DIR/js/typeahead.js -o /tmp/tmp.js
cp /tmp/tmp.js $DIR/js/typeahead.js
yui-compressor $DIR/programs.css -o /tmp/tmp.css
cp /tmp/tmp.css $DIR/programs.css
yui-compressor $DIR/css/common.css -o /tmp/tmp.css
cp /tmp/tmp.css $DIR/css/common.css
yui-compressor $DIR/search.css -o /tmp/tmp.css
cp /tmp/tmp.css $DIR/search.css
# <OTHER_PROJECT> PROJECT
# cp ../../../<OTHER_PROJECT>/docker/nginx/build/<OTHER_PROJECT> build/ -r
# cp ../../../<OTHER_PROJECT>/docker/nginx/build/<OTHER_PROJECT>_nginx.conf build/ -r
# build docker image
sudo docker build -t funeslab/nginx-cos-elec:v0 .
