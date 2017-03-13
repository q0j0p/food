import requests
import json
import re
import pprint
import time
import pymongo
BASE_URL = "https://api.nal.usda.gov/ndb/list"

def get_usda_ndb_listdata(offset=0):
    params = {"lt":"f",
              "sort":"id",
              "max":"50",
              "offset":str(offset),
              "api_key":"PDddrH73wtpvf3gAtRyQUXVWlv80tON7RBFp2xlm"}
    return requests.get(BASE_URL, params=params)



if __name__ == "__main__":
    # connect to the hosted MongoDB instance
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.usda_ndb
    coll = db.food_list
    for n in xrange(0,184022,50): #184,022 food items in database; list of 50 at a time.
      t = get_usda_ndb_listdata(offset=n)
      coll.insert_many(t.json()['list']['item'])
      print "inserted {} batches, starting with {}\n".format(n,
                                                            t.json()['list']['item'][0])

      time.sleep(0)
