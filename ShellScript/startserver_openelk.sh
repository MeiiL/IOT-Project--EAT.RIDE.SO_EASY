#!/bin/bash

sudo sysctl -w vm.max_map_count=262144
sudo docker start kafka-elk
sudo docker exec -it kafka-elk /bin/bash 
if [ $? -eq 0];then
  sh startall_elk_kafka.sh
else
  echo "waiting docker start"
  sleep 5
fi
