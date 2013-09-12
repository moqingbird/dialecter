#!/usr/bin/env python

import sys
import traceback
import pymongo
sys.path.append(".")

from pymongo_hadoop import BSONMapper
from pymongo import MongoClient

def mapper(documents):
  try:
     connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
     db=connection.dialect_db
     threshold=float(db.parameters.find_one({"name":"classification_threshold"},{"_id":0,"value":1})["value"])
     res_len=-1
     for doc in documents:
        if res_len == -1:
          res_len=len(doc["predicted_region"])
        top=doc["predicted_region"][res_len-1][1]
        second=doc["predicted_region"][res_len-2][1]
        max_region="UNKNOWN"
        if abs((top-second)/second) >= threshold:
           max_region=doc["predicted_region"][res_len-1][0]
           yield {"_id":doc["actual_region"],
                 "max_region":max_region}
  except:
    print >> sys.stderr, "Unexpected map error "
    traceback.print_exc()
    raise


print >> sys.stderr, "Start Mapping"
try:
  BSONMapper(mapper)
except Exception, e:
  print >> sys.stderr, "something went wrong"
  print >> sys.stderr, e
  raise
print >> sys.stderr, "Done Mapping."

