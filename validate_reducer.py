#!/usr/bin/env python

import sys
import traceback
import pymongo
sys.path.append(".")

from pymongo_hadoop import BSONReducer
from pymongo import MongoClient
from RegionList import RegionList

def reducer(key, values):
  try:
    print >> sys.stderr , "Start Reduce"
    rl=RegionList()
    rl.populate(False)
    print >> sys.stderr , "Got region list"
    connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
    db=connection.dialect_db
    k=int(db.parameters.find_one({"name":"k"},{"_id":0,"value":1})["value"])
    print >> sys.stderr , "Got k"
    connection.close()
    _counts  = [0 for i in range(0,len(rl.regions))]
    count=0
    for v in values:
       if count < 5:
          print >> sys.stderr, str(key["k_group"])+","+key["region"]+", maxregion: "+v["max_region"]+", seq: "+str(rl.get(v["max_region"]).seq)
       _counts = [_counts[i]+1 if i==rl.get(v["max_region"]).seq else _counts[i] for i in range(0,len(rl.regions))]
    return {'_id': key,'totals':  _counts}
  except:
    print >> sys.stderr, "Unexpected reduce error " 
    traceback.print_exc()
    err_file=open("~\\dialecter\\reduce_err.txt","w")
    traceback.print_exception(sys.exc_info()[0],
                              sys.exc_info()[1],
                              sys.exc_info()[2],
                              limit=None,
                              file=err_file)
    err_file.close()
    raise

print >> sys.stderr, "Start Reduce"
BSONReducer(reducer)
print >> sys.stderr, "Done Reduce"

