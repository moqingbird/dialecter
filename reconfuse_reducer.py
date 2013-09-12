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
    print >> sys.stderr , "In  Reducer"
    rl=regions={"NI": 1,"COR": 2,"BRIS": 3,"CORN": 4,"ABN": 5,"BRAD": 6,"BRGT": 7,"BRNM": 8,"BRUM": 9,"CANT": 10,"CAR": 11,"DUB": 12,"DUND": 13,"EDB": 14,"ESX": 15,"GAL": 16,"GLAS": 17,"HULL": 18,"LEED": 19,"LEIC": 20,"LINC": 21,"LVP": 22,"MANC": 23,"NEWC": 24,"NORW": 25,"NTHM": 26,"OXF": 27,"PORT": 28,"YORK": 29,"SHEF": 30,"SOUTH": 31,"STAN": 32,"SURY": 33,"UNKNOWN":34}
    connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
    db=connection.dialect_db
    k=int(db.parameters.find_one({"name":"k"},{"_id":0,"value":1})["value"])
    connection.close()
    _counts  = [0 for i in range(0,len(rl))]
    count=0
    for v in values:
       #if count < 5:
       #   print >> sys.stderr, str(key["k_group"])+","+key["region"]+", maxregion: "+v["max_region"]+", seq: "+str(rl.get(v["max_region"]).seq)
       if v["max_region"]!="None":
          _counts = [_counts[i]+1 if i==rl[v["max_region"])] else _counts[i] for i in range(0,len(rl))]
       else:
           print >> sys.stderr,  str(key["k_group"])+","+key["region"]+", maxregion: "+v["max_region"]
    return {'_id': key,'totals':  _counts}
  except:
    print >> sys.stderr, "Unexpected reduce error " 
    traceback.print_exc()
    err_file=open("reduce_err.txt","w")
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

