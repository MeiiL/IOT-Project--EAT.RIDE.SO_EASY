from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math


class Recommendation :
    '''
    to return supply points near the user
    Args: client user
    '''
    user_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                   0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                   0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                   0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0]
    vector_base = np.mat(user_vector)

    def __init__(self,client, collection):
        self.client = client
        self.iot_collection = collection

    def get_location(self):
        '''
        load gps data from mongoDB.
        :return:  get_supply_point
        '''
        for record in [loc for loc in self.iot_collection.find().sort("_id", -1).limit(1)]:
            location = {"x": record["lat"], "y": record["lng"]}
            # location = {"x":24.967742,"y":121.1895113}
            # print(location)
        return self.get_supply_point(location)

    def get_supply_point(self, location):
        '''
        load supply points' data from MongoDB by location
        and utilize cosine similarity to choose the matching supply points
        :param location: user current location
        :return: final_recommend
        '''
        cuisines_db = self.client["cuisines"]
        cuisines_collection = cuisines_db["foodIPEEN"]
        show_data = {"name": 1, "add": 1, "tel": 1, "rating": 1, "avg_exp": 1, "latitude": 1,
                     "tag": 1, "longitude": 1, "url": 1 , 'tag_vector': 1, "_id": 0}
        supply_points = cuisines_collection.find(
            {"longitude": {"$gte": float(location["y"]) - 0.03, "$lte": float(location["y"]) + 0.03},
             "latitude": {"$gte": float(location["x"]) - 0.03, "$lte": float(location["x"]) + 0.03},
             "rating": {"$gte": 3.4}},
            show_data)
        supply_points = [supply_point for supply_point in supply_points]
        # 逐店計算cos similarity(user的tag_vector,店家的tag_vector)
        for supply_point in supply_points:
            supply_point_vector = np.mat(supply_point["tag_vector"])
            cos_sim = cosine_similarity(self.vector_base, supply_point_vector)
            supply_point["cos_sim"] = cos_sim[0, 0]
            supply_point.pop('tag_vector', None)
        return self.final_recommend(supply_points)

    def final_recommend(self, supply_points):
        '''
        sort the supply points and recommend
        :param supply_points: supply points
        :return:
        '''
        supply_point_with_nan = [i for i in supply_points if math.isnan(i["cos_sim"])]
        supply_point_without_nan = [i for i in supply_points if not math.isnan(i["cos_sim"])]
        supply_points_final = sorted(supply_point_without_nan, key=lambda x: x["cos_sim"], reverse=True)
        supply_points_final.extend(supply_point_with_nan)
        # TOP 10 Stores we recommend
        supply_points_recommend = supply_points_final[:10]
        print(supply_points_recommend)
        return supply_points_recommend

    def recommendation(self):
        '''
        start to go through recommendation system
        :return: get_location
        '''
        return self.get_location()

def main():
    client = MongoClient('localhost', 27017)
    db = client['iot']
    collection = db['user2']
    recommend = Recommendation(client, collection)
    supply_points = recommend.recommendation()
    # for i in supply_points :
    print(supply_points)

if __name__ == "__main__":
    main()
