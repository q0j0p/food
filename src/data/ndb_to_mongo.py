import requests
import json
import re
import pprint
import time
import pymongo
import pdb
BASE_URL = "https://api.nal.usda.gov/ndb/list"
USDA_API_KEY = 'PDddrH73wtpvf3gAtRyQUXVWlv80tON7RBFp2xlm'

class USDA_data_collector(object):
    def __init__(self):
        self.api_key = USDA_API_KEY
        self.url = BASE_URL

    def get_usda_ndb_foodlist(offset=0, **kwargs):
        params = {"lt":"f",
                  "sort":"id",
                  "max":"50",
                  "offset":str(offset),
                  "api_key":"PDddrH73wtpvf3gAtRyQUXVWlv80tON7RBFp2xlm"}
        db = client.usda_ndb
        coll = db.nutrient_list
        print "start collection \n"
        for n in xrange(0,99800,50): #184,022 food items in database; list of 50 at a time.
          t = get_usda_ndb_listdata(offset=n)
          print "status: {}\n".format(str(t))
    #      pdb.set_trace()
          coll.insert_many(t.json()['list']['item'])
          print "inserted {} entries\nstarting with {}\n".format(n,
                                                                t.json()['list']['item'][0])
          time.sleep(0)



def get_usda_ndb_listdata(offset=0, **kwargs):
    params = {"lt":"f",
              "sort":"id",
              "max":"50",
              "offset":str(offset),
              "api_key":"PDddrH73wtpvf3gAtRyQUXVWlv80tON7RBFp2xlm"}
    return requests.get(BASE_URL, params=params)


def get_usda_ndb_fooddata(start=0, **kwargs):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.usda_ndb

    foodid_list = db.food_list.distinct('id')

    coll = db.food_item

    URL = "https://api.nal.usda.gov/ndb/V2/reports"
    print "length of food list: {}".format(len(foodid_list))
#    time.sleep(2400)
    for n in xrange(start,len(foodid_list),50):
        params = {"ndbno": foodid_list[n:n+50],
            "type":"f",
            "api_key":USDA_API_KEY}
        t = requests.get(URL, params=params)
        print "status is {}".format(str(t))
        coll.insert_many(t.json()['foods'])
        print "inserted {} entries".format(n)
        time.sleep(0)
#    return "{} documents in {}, {}".format()





if __name__ == "__main__":
    # connect to the hosted MongoDB instance
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.usda_ndb
    coll = db.food_item
    print "start collection \n"
    for n in xrange(0,184022,50): #184,022 food items in database; list of 50 at a time.
      t = get_usda_ndb_listdata(offset=n)
      print "status: {}\n".format(str(t))
#      pdb.set_trace()
      coll.insert_many(t.json()['list']['item'])
      print "inserted {} entries\nstarting with {}\n".format(n,
                                                            t.json()['list']['item'][0])
      time.sleep(0)
