rm -rf build
mkdir build
cp install.sh build/
sudo docker save -o build/funeslab_uwsgielec.tar funeslab/uwsgielec:v0
sudo docker save -o build/funeslab_nginx-cos-elec.tar funeslab/nginx-cos-elec:v0
cp elasticsearch/run.sh build/run_elasticsearch.sh
cp elecprogweb/run.sh build/run_elecprogweb.sh
cp nginx/run.sh build/run_nginx.sh
echo "Remember to copy elasticsearch.tgz to build!"
echo "Remember to copy elasticsearch.tgz to build!"
