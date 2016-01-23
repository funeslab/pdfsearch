THIS_DIR=`pwd`
sudo docker load -i funeslab_uwsgielec.tar
sudo docker load -i funeslab_nginx-cos-elec.tar
sudo mkdir -p  /var/container/elasticsearch/data
sudo chmod 755 /var/container/elasticsearch/ -R
sudo chmod 777 /var/container/elasticsearch/data -R
cd /
sudo tar -xvzf $THIS_DIR/elasticsearch.tgz
cd $THIS_DIR
sudo bash run_elasticsearch.sh
sudo bash run_elecprogweb.sh
sudo bash run_nginx.sh
