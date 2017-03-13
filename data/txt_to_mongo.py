# parse finefoods.txt (SNAP Amazon reviews data) into json format

import simplejson
import io
import pymongo
TXTFILE = 'finefoods.txt'
PATH_TO_TXTFILE = 'sources/finefoods.txt'


def txt_parse(filename):
    """

    For SNAP (Stanford Network Analysis Project) datafiles in .txt files:
        Parses entries into JSON format.

    Parameters
    ---------
    filename : string
        path plus name of .txt file

    Returns
    -------
    generator
        object yields entries in json format
    """

    f = open(filename, 'r')
    entry = {}
    for l in f:
    l = l.strip()
    colonPos = l.find(':')
    if colonPos == -1:
      yield entry
      entry = {}
      continue
    eName = l[:colonPos]
    rest = l[colonPos+2:]
    entry[eName] = unicode(rest, errors='ignore') # catch non-UTF-8 character encodings
    yield entry


'''
Script to insert all entries in mongo database
'''
if __name__ == '__main__':
    gen = txt_parse(PATH_TO_TXTFILE+TXTFILE) # instantiate generator object
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.areviews
    coll = db.reviews
    for item in gen:
    coll.insert_one(item)
