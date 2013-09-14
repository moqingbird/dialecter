#!/usr/bin/env python

import sys
import traceback

import math
import pymongo
sys.path.append(".")
from pymongo_hadoop import BSONReducer
from pymongo import MongoClient
from MongoConnection import MongoConnection

def reducer(key, values):
  try:
    db=MongoConnection().get().dialect_db
    stats=db.ngram_stats.find_one({"_id":key})
    sum_sqr=0
    count=0
    for v in values:
      sum_sqr+=v["sqr"]
      count+=1

    if count < stats["region_count"]:
       sum_sqr+=(stats["region_count"]-count) * pow(math.log(sys.float_info.min)-stats["mean"],2)
       
    return {"_id":key, 
            "mean": stats["mean"],
            "region_count":stats["region_count"],
            "sum_squares": sum_sqr, 
            "variance": sum_sqr/stats["region_count"],
            "std_dev": math.sqrt(sum_sqr/stats["region_count"])}
  except:
    print >> sys.stderr, "Unexpected reduce error "
    traceback.print_exc()
    raise

print >> sys.stderr, "Start Reduce"
BSONReducer(reducer)
print >> sys.stderr, "Done Reduce"

