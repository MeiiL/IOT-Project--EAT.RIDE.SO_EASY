#!/bin/bash

#sudo apt-get remove docker docker-engine -y
#sudo apt-get remove docker.io -y
sudo apt-get install \
    linux-image-extra-$(uname -r) \
    linux-image-extra-virtual
sudo apt-get install \
  apt-transport-https \
  ca-certificates \
  curl \
  software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
sudo apt-get update -y
sudo apt-get install docker-ce -y
sudo groupadd docker 
sudo usermod -aG docker $USER
sudo systemctl enable docker 
sudo docker --version
sudo mkdir ~/elk-data
sudo mkdir ~/projectfile
sudo docker pull meiil/kafka-elk
#sudo docker pull mongo
sudo sysctl -w vm.max_map_count=262144
sudo docker run -p 5601:5601 -p 9200:9200 -p 5044:5044 -p 9092:9092 -d -v ~/elk-data:/var/lib/elasticsearch -v ~/projectfile:/root/projectfile --name kafka-elk meiil/kafka-elk:0.0.0
#sudo docker run -d --name mongo-django  -p 27017:27017 mongo