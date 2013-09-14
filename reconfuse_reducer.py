#!/usr/bin/env python

import sys
import traceback
import pymongo
sys.path.append(".")

from pymongo_hadoop import BSONReducer
from pymongo import MongoClient
from RegionList import RegionList
from MongoConnection import MongoConnection

def reducer(key, values):
  try:
    print >> sys.stderr , "In  Reducer"
    rl={"NI":0,"COR":1,"BRIS":2,"CORN":3,"ABN":4,"BRAD":5,"BRGT":6,"BRNM":7,"BRUM":8,"CANT":9,"CAR":10,"DUB":11,"DUND":12,"EDB":13,"ESX":14,"GAL":15,"GLAS":16,"HULL":17,"LEED":18,"LEIC":19,"LINC":20,"LVP":21,"MANC":22,"NEWC":23,"NORW":24,"NTHM":25,"OXF":26,"PORT":27,"YORK":28,"SHEF":29,"SOUTH":30,"STAN":31,"SURY":32,"UNKNOWN":33}
    db=MongoConnection().get().dialect_db
    k=int(db.parameters.find_one({"name":"k"},{"_id":0,"value":1})["value"])
    _counts  = [0 for i in range(0,len(rl))]
    count=0
    for v in values:
       #if count < 5:
       #   print >> sys.stderr, str(key["k_group"])+","+key["region"]+", maxregion: "+v["max_region"]+", seq: "+str(rl.get(v["max_region"]).seq)
       if v["max_region"]!="None":
          _counts = [_counts[i]+1 if i==rl[v["max_region"]] else _counts[i] for i in range(0,len(rl))]
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

