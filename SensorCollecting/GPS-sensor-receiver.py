# -*- coding: UTF-8 -*-



import serial

import pynmea2

import os

import csv

from datetime import datetime

from pymongo import MongoClient

import json

from bson import json_util

from kafka import KafkaProducer

from math import radians, cos, sin, asin, sqrt  

import sys

 

def latlng_transto_distance(old_longlati, longitude2, latitude2):

    """ 

    Calculate the distance between two points  

    on the earth (specified in decimal degrees)

    transform Latitude and longitude into distance(meters)

    """  

    if longitude2 == "-" :

        distance = "-"

    elif old_longlati == ["-","-"] :

        distance = "-"

    else:

        # 用 radians 轉換成弧度

        long1, lat1, long2, lat2 = map(radians, [old_longlati[0], old_longlati[1], longitude2, latitude2])  

        old_longlati[0] = longitude2

        old_longlati[1] = latitude2

        # haversine公式  

        delta_longitude = long2 - long1   

        delta_latitude = lat2 - lat1   

        a = sin(delta_latitude/2)**2 + cos(lat1) * cos(lat2) * sin(delta_longitude/2)**2  

        c = 2 * asin(sqrt(a))   

        r = 6378.1 # 地球平均半徑(km)

        distance = c * r * 1000 # 轉成公尺

    return distance

    

def transto_speed(distance):

    if distance == "-" :

        speed = "-"

    else :

        speed = distance * 3.6

    return speed

    

    

def gps_convert(longitude, latitude, altitude):

    if longitude == "" :

        lng = "-"

        lat = "-"

        Altitude = "-"

    else :

        lat_int = int(float(latitude)/100)

        lat_point = float((float(latitude)/100 - lat_int)/0.6)

        lat = float(lat_int + lat_point)

        lng_int = int(float(longitude)/100)

        lng_point = float((float(longitude)/100 - lng_int)/0.6)

        lng = float(lng_int + lng_point)  

        Altitude = altitude

        

    return lng, lat, Altitude

    

    

def parseGPS(data):

    if data.find('GGA') > 0:   

        try:

            msg = pynmea2.parse(data)

            lng, lat, Altitude = gps_convert(msg.lon, msg.lat, msg.altitude)

            print(old_data)

            #print "Timestamp_GPS: %s -- Lat: %s -- Lon: %s -- Altitude: %s %s" % (msg.timestamp,lat,lng,Altitude,msg.altitude_units)

            distance = latlng_transto_distance(old_data,lng,lat)

            speed = transto_speed(distance)

            print(speed)

            time_RPI = datetime.now().isoformat() #recording RPItime

            filename = time_RPI.replace("-","").replace("T","-").replace(":","").split(".")[0]+"-gps"

            csvfile = csv.writer(open('./data/raw_data/gps/{}.csv'.format(filename), 'a'))

            csvfile.writerow(['UserID','Timestamp_RPI', 'Timestamp_GPS', 'lat', 'lng', 'Altitude', 'Distance', 'Speed'])

            csvfile.writerow(['user1', time_RPI, msg.timestamp, lat, lng, Altitude, distance, speed])  # csv write by row



        except KeyboardInterrupt:

            sys.exit(0)

        except:

            pass





def main():

    

    while True:

        data = serialPort.readline()

        parseGPS(data)





if __name__ == '__main__':

    serialPort = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)

    old_data = [121.19179266666,24.967609166666]

    main()










