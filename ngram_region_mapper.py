#!/usr/bin/env python

import sys
import traceback
import pymongo
sys.path.append(".")

from pymongo import MongoClient
from pymongo_hadoop import BSONMapper
from RegionList import RegionList

def mapper(documents):
  try:
    delimiter="[[$$$]]"
    n=3
    k_folds=10
    rl=RegionList()
    rl.populate(False)
    connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
    db=connection.dialect_db
    rpub_regions={}
    rpub_cur=db.region_pubs.find({},{"_id":1,"region":1})
    for rpub in rpub_cur:
      if rl.regions.has_key(rpub["region"]):
          rpub_regions[rpub["_id"]]=rpub["region"]
    connection.close()
    for doc in documents:
        if not doc["exclude"]:
            words=doc["clean_text"].strip().split()        
            for i in range(0,len(words)):#-len(delimiter.split())):
                for j in range(1,n+1):
                    if i+j > len(words) or (j > 2 and words[i+j-2] == delimiter):
                        break # don't span sentence ends
                    yield {'_id': {'region':rpub_regions[doc["region_pub"]],
                                    'ngram':" ".join(words[i:i+j]),
                                    'n':j}, 
                            'k_groups': [0 if k==doc["k_group"] else 1 for k in range(0,k_folds)]}
  except:
    print >> sys.stderr, "Unexpected map error " 
    traceback.print_exc()
    raise


print >> sys.stderr, "Start Mapping"
BSONMapper(mapper)
print >> sys.stderr, "Done Mapping."
