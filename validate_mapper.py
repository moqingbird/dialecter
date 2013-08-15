#!/usr/bin/env python

import sys
from datetime import datetime

import traceback
import pymongo
sys.path.append(".")

from pymongo_hadoop import BSONMapper
from pymongo import MongoClient
from RegionList import RegionList
from Post import Post

def mapper(documents):
  try:    
    rl=RegionList()
    rl.populate(False,True,True)
    connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
    db=connection.dialect_db
    n=int(db.parameters.find_one({"name":"n"},{"_id":0,"value":1})["value"])
    k=int(db.parameters.find_one({"name":"k"},{"_id":0,"value":1})["value"])
    rpub_regions={}
    rpub_cur=db.region_pubs.find({"exclude":False},{"_id":1,"region":1})
    for rpub in rpub_cur:
      if rl.regions.has_key(rpub["region"]):
          rpub_regions[rpub["_id"]]=rpub["region"]
    connection.close()
    count=0
    for doc in documents:
        if doc["exclude"]==False and rpub_regions.has_key(doc["region_pub"]):
           post=Post(doc["_id"],rpub_regions[doc["region_pub"]], doc["clean_text"],0.75,True)
           post.set_kgroup(doc["k_group"])
           print >> sys.stderr, str(datetime.now()) + doc["_id"]
           try:
             post.calc(db,rl,n)
           except:
             print >> sys.stderr, doc["_id"]
             raise
           print >> sys.stderr, str(datetime.now())
           yield {'_id': {'k_group': doc["k_group"],
                          'region': post.regionId},
                 'max_region':post.maxRegion}
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

