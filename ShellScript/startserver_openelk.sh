#!/bin/bash

sudo sysctl -w vm.max_map_count=262144
sudo docker start 48
sudo docker exec -it 48 /bin/bash 
if [ $? -eq 0];then
  sh startall_elk_kafka.sh
else
  echo "waiting docker start"
  sleep 5
fi
