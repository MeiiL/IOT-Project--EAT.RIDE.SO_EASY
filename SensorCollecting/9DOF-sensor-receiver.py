import smbus
import math
import time
import csv
import os
from datetime import datetime
from pymongo import MongoClient
import json



# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

def getSensorData():
    while True:
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)

        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        time_RPI = datetime.now().isoformat() #recording RPItime

        return (str(time_RPI),int(gyro_xout), int(gyro_yout),int(gyro_zout),int(accel_xout), int(accel_yout),int(accel_zout),int(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)),int(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)))
        time.sleep(0.1)


def main():
    
    while True:
        try:
            time_RPI, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, rotate_x, rotate_y = getSensorData()
            filename = time_RPI.replace("-","").replace("T","-").replace(":","").split(".")[0]+"-9dof"
            csvfile = csv.writer(open('./data/raw_data/9dof/{}.csv'.format(filename), 'a'))
         
            #csvfile.writerow(['UserID','Timestamp_RPI','Gyro_x', 'Gyro_y', 'Gyro_z', 'Accel_x', 'Accel_y', 'Accel_z', 'Rotate_x', 'Rotate_y']) 
           
            csvfile.writerow(['user1',time_RPI, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, rotate_x, rotate_y]) 
            
            print ('user1',time_RPI, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, rotate_x, rotate_y) 
         
            time.sleep(0.2) 
        except:
            print ('exiting.')
            break
# call main
if __name__ == '__main__':
    main()


