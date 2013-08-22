#!/usr/bin/env python

import sys
import traceback

import pymongo
sys.path.append(".")
from pymongo_hadoop import BSONReducer
from pymongo import MongoClient

def reducer(key, values):
  try:
    sum_sqr=0
    for v in values:
      sum_sqr+=v["sqr"]
    return {"_id":key, "sum_squares": sum_sqr, "std_dev": math.sqrt(sum_sqr)}
  except:
    print >> sys.stderr, "Unexpected reduce error "
    traceback.print_exc()
    raise

print >> sys.stderr, "Start Reduce"
BSONReducer(reducer)
print >> sys.stderr, "Done Reduce"

