#!/usr/bin/env python

import sys
from datetime import datetime

import traceback
import pymongo
sys.path.append(".")

from pymongo_hadoop import BSONMapper
from pymongo import MongoClient
from RegionList import RegionList
from Region import Region
from Post import Post
from MongoConnection import MongoConnection

def mapper(documents):
  try:    
    rl=RegionList()
    rl.populate(False,True,True)

    rl2=RegionList()
    rl2.populate(False,False,False)

    db=MongoConnection().get().dialect_db
    n=int(db.parameters.find_one({"name":"n"},{"_id":0,"value":1})["value"])
    k=int(db.parameters.find_one({"name":"k"},{"_id":0,"value":1})["value"])
    rpub_regions={}
    for region in rl.regions:
       children=[region]
       Region.getChildren(region,children,db)
       for child in children:
          #rpub_cur=db.region_pubs.find({"exclude":False},{"_id":1,"region":1})
          rpub_cur=db.region_pubs.find({"region":child},{"_id":1,"region":1})
          for rpub in rpub_cur:
            #if rl.regions.has_key(rpub["region"]):
              rpub_regions[rpub["_id"]]=rpub["region"]
    valid_authors={}
    auth_cur=db.authors.find({"pubgroup":"REDDIT","selfClassification": {"$nin": ["unknown","conflict",""]}})
    for auth in auth_cur:
      valid_authors[auth["_id"]]=auth["selfClassification"]
    count=0
    for doc in documents:
       if doc["exclude"]==False and  valid_authors.has_key(doc["author"]):
           post=Post(doc["_id"],valid_authors[doc["author"]], doc["clean_text"],0.75,True)
           post.set_kgroup(doc["k_group"])
           print >> sys.stderr, str(datetime.now()) + doc["_id"].encode("utf-8")
           try:
             post.calc(db,rl,n)
           except:
             print >> sys.stderr, doc["_id"]
             raise
           print >> sys.stderr, str(datetime.now())
           #if post.maxRegion != rl2.get(post.regionId).calcParent:
           #   db.wrong.save({"_id": post.id, "actual_region": rl2.get(post.regionId).calcParent, "predicted_region": post.maxRegion})
           db.results.save({"_id": post.id, 
                            "actual_region": valid_authors[doc["author"]],
                            "predicted_region": post.sortedRegions})
           yield {'_id': {'k_group': doc["k_group"],
                          'region': rl2.get(post.regionId).calcParent},
                 'max_region':post.sortedRegions[len(post.sortedRegions)-1][0]}
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

