#!/usr/bin/env python

import sys
import pymongo
sys.path.append(".")

import traceback

from pymongo_hadoop import BSONMapper
from pymongo import MongoClient

def mapper(documents):
  try:
    connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
    db=connection.dialect_db
    prev_ngram="empty"
    mean=0
    for doc in documents:
     if doc["exclude"] == False:
      try:
        if doc["_id"]["ngram"] != prev_ngram:
          mean=db.ngram_stats.find_one({"_id": doc["_id"]["ngram"]})["mean"]
          prev_ngram= doc["_id"]["ngram"]
        yield {"_id": doc["_id"]["ngram"], "sqr": pow(doc["total_likelihood"]-mean,2)}
      except:
        print >> sys.stderr, "doc id ngram: "+doc["_id"]["ngram"]
        raise
  except:
    print >> sys.stderr, "Unexpected map error "
    traceback.print_exc()
    raise


print >> sys.stderr, "Start Mapping"
try:
  BSONMapper(mapper)
except Exception, e:
  print >> sys.stderr, "something went wrong"
  traceback.print_exc()

