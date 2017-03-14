
Gather all data from UDSA NDB database: 

-capture error msg when gathering NDB API data  

```Traceback (most recent call last):
  File "ndb_to_mongo.py", line 26, in <module>
    coll.insert_many(t.json()['list']['item'])
    ```
    
KeyError: 'list'
HTTP stats code is 429: Too many requests.  

-find out difference between food list and food items. 

## Mongodb and pymongo 

