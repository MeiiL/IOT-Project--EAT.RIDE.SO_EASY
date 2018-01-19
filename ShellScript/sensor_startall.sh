#!/bin/bash

sudo netstat -nlp | grep 9092
if [ $? -eq 0 ]; then
    echo "Port 9092 connected"
else
    read -p 'Input Bastion IP:' IP
    eval $(ssh-agent)
    chmod 600 /home/pi/pem/general.pem
    chmod 600 /home/pi/pem/bastion.pem
    ssh-add /home/pi/pem/general.pem
    ssh -A -i /home/pi/pem/bastion.pem -NfL 27017:10.10.220.229:27017 ec2-user@${IP} #connecting mongodb
    ssh -A -i /home/pi/pem/bastion.pem -NfL 9092:10.10.220.126:9092 ec2-user@${IP} #connecting kafka
fi

python GPS-sensor-receiver.py &
python3 9DOF-sensor-receiver.py &
python3 Heartbeat-sensor-receiver.py &
python3 SensorDataSend.py &
echo "Sensor Start"
top