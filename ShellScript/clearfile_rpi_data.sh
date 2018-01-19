#!/bin/bash

read -p 'Are you sure wanna clear the 9dof/gps file? (y/n) :' check
if [ ${check} -eq 'y' ]; then
    rm ~/data/raw_data/9dof/*.csv
    rm ~/data/raw_data/gps/*.csv
    echo "file cleared, can start raspberry pi now."
else
    echo "no worries, see ya!"
fi


