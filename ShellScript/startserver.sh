#!/bin/bash

sudo sysctl -w vm.max_map_count=262144
sudo docker start kafka-elk
sudo docker exec -it kafka-elk /bin/bash 
