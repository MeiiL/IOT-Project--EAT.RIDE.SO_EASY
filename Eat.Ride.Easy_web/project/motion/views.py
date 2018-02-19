from django.shortcuts import render
from pymongo import MongoClient
from . import recommendation

# Create your views here.
def motion(request):
    return render(request, 'motion/motion.html',{})

def gmap(request):

    client = MongoConnection.getConnection()
    db = client['iot']  # db name
    collection = db['user3']  # collection name
    datas = collection.find() # motion datas
    
    recommend = recommendation.Recommendation(client,collection)
    supply_points = recommend.recommendation() # recommendation datas
    return render(request, 'gmap/gmap.html',{'datas':datas,'supply_points':supply_points})

class MongoConnection(object):
    client = None

    @staticmethod
    def getConnection():
        if MongoConnection.client is None:
            MongoConnection.client = MongoClient("mongodb://127.0.0.1:27017")
            return MongoConnection.client
        else:
            return MongoConnection.client
