#!bin/bash

sudo yum remove docker \
	  docker-common \
	    container-selinux \
	      docker-selinux \
	        docker-engine \
		  docker-engine-selinux
sudo yum install -y yum-utils \
	  device-mapper-persistent-data lvm2
sudo yum-config-manager \
	  --add-repo \
	    https://download.docker.com/linux/centos/docker-ce.repo
sudo yum-config-manager --enable docker-ce-edge 
#edge version
sudo yum makecache fast
sudo yum install -y docker-ce
sudo systemctl start docker
sudo docker --version
