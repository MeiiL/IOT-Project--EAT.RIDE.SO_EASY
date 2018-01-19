
# coding: utf-8

# In[ ]:


import pickle
import os
import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import normalize
import random
import time
from kafka import KafkaProducer
from pymongo import MongoClient
from kafka.errors import KafkaError
import json

class Kafka_producer():
    def __init__(self, kafkahost, kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers='{kafka_host}:{kafka_port}'.format(kafka_host = self.kafkaHost,kafka_port = self.kafkaPort))    

    def sendjsondata(self, params):
        try:
            params_message = json.dumps(params)
            producer = self.producer
            print(self.kafkatopic)
            print(params_message)
            producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send(self.kafkatopic, params_message)
            producer.flush()
        except KafkaError as e:
            print(e)
def main():   

    # Random Forest Modeling    
    with open('/home/pi/data/save/pkl_objects/forest_model.pkl','rb') as r:
        forest_slope_model = pickle.loads(r.read())
    with open('/home/pi/data/save/pkl_objects/forest_bumpy_model.pkl','rb') as r:
        forest_bumpy_model = pickle.loads(r.read())
    dir_path = "/home/pi/data/raw_data/9dof/"
    os.listdir(dir_path)

    # Kafka connecting
    producer = Kafka_producer("127.0.0.1", 9092, "test") 
    # Mongo DB connecting
    client = MongoClient('127.0.0.1',27017)
    db = client['iot']

    while True:    
        columns = ["UserID","Timestamp_RPI","Gyro_x","Gyro_y","Gyro_z","Accel_x","Accel_y","Accel_z","Rotate_x","Rotate_y"]
        df = pd.DataFrame([["1","1",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1]],columns=columns)
        file_use = os.listdir(dir_path)
        file_use = sorted(file_use)
        if len(file_use)>4:
            for file in file_use[:5]:
                df = df.append(pd.read_csv(dir_path + file,names=columns),ignore_index=True)
            #for slope motion classification

            normal= normalize(df.iloc[1:,2:8], norm='l2', axis=1, return_norm=True)
            df_TMP = pd.DataFrame(normal[0]).var().values.reshape(1,-1)
            predicit = forest_slope_model.predict(df_TMP)
            df["Motion_Label"] = predicit[0]
            
            #for bumpy motion classification
            df["Bumpy_Label"] = "0"
            data_chk = df.shape[0]%2
            _shape = df.shape[0]
            if data_chk == 0:
                _shape = _shape - 1
            for i in range(1,_shape,2):
                normal= normalize(df.iloc[i:i+2,2:8], norm='l2', axis=1, return_norm=True)
                df_TMP = pd.DataFrame(normal[0]).var().values.reshape(1,-1)
                predicit = forest_bumpy_model.predict(df_TMP)
                df.iloc[i:i+2,11] = predicit[0]
            if data_chk == 1:
                df.iloc[-1,11] = predicit[0]
                
#             df["Bumpy_Label"] = "0"
#             for i in range(1,df.shape[0]):
#                 print(df.iloc[i,2:8])
#                 normal= normalize([df.iloc[i,2:8]], norm='l2', axis=1, return_norm=True)
#                 df_TMP = pd.DataFrame(normal[0]).values.reshape(1,-1)
#                 print(df_TMP)
#                 predicit = forest_bumpy_model.predict(df_TMP)
#                 df.iloc[i,11] = predicit[0]

            #for gps data append

            df["lat"] = None
            df["lng"] = None
            df["Altitude"] = None
            df["Distance"] = None
            df["Speed"] = None

            gps_used_file = set()
            for i in range(1,df.shape[0]):
                gps_file_name = df.iloc[i,1].replace("-","").replace("T","-").replace(":","").split(".")[0]
                chk = True
                count = 0
                while chk:
                    try:
                        with open("/home/pi/data/raw_data/gps/{}-gps.csv".format(gps_file_name), "r") as r:
                            for j in range(2):
                                gps_data =r.readline().replace("\n","").split(",")

                            df.iloc[i,12] = gps_data[3]
                            df.iloc[i,13] = gps_data[4]
                            df.iloc[i,14] = gps_data[5]
                            df.iloc[i,15] = gps_data[6]
                            df.iloc[i,16] = gps_data[7]
                            gps_used_file.add(gps_file_name)
                            chk = False
                    except:
                        if count == 1:
                            break
                        count +=1
                        time.sleep(0.7)
                        pass
            # data consolidated 
            for i in range(1,df.shape[0]):
                dof_record = {
                    "UserID": df.iloc[i,0],
                    "Timestamp_RPI": df.iloc[i,1],
                    "Gyro_x": df.iloc[i,2],
                    "Gyro_y": df.iloc[i,3],
                    "Gyro_z": df.iloc[i,4],
                    "Accel_x": df.iloc[i,5],
                    "Accel_y": df.iloc[i,6],
                    "Accel_z": df.iloc[i,7],
                    "Rotate_x": df.iloc[i,8],
                    "Rotate_y": df.iloc[i,9],
                    "Motion_Label": df.iloc[i,10],
                    "Bumpy_Label": df.iloc[i,11],
                    "lat": df.iloc[i,12],
                    "lng": df.iloc[i,13],
                    "Altitude": df.iloc[i,14],
                    "Distance": df.iloc[i,15],
                    "Speed": df.iloc[i,16]
                }
                # send to kafka
                params = dof_record
                producer.sendjsondata(params)
                # send to mongodb
                db.user1.insert_one(dof_record)
            df.iloc[1:,:].to_csv("/home/pi/data/final_data/{}".format(file_use[0]),index=False)
            list(map(lambda file: os.remove(dir_path + file),[file for file in file_use[:5]]))
            list(map(lambda file: os.remove("/home/pi/data/raw_data/gps/{}-gps.csv".format(file)),[file for file in gps_used_file]))   

# call main
if __name__ == '__main__':
    main()

