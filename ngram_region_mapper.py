#!/usr/bin/env python

import sys
import traceback
import pymongo
sys.path.append(".")

from pymongo import MongoClient
from pymongo_hadoop import BSONMapper
from RegionList import RegionList
from MongoConnection import MongoConnection

def mapper(documents):
  try:
    sentence_end="[[$$$]]"
    question_end="[[???]]"
    delimiters=[sentence_end,question_end]
    
    n=3
    k_folds=10
    rl=RegionList()
    rl.populate(False)
    db=MongoConnection().get().dialect_db
    rpub_regions={}
    rpub_cur=db.region_pubs.find({},{"_id":1,"region":1})
    for rpub in rpub_cur:
      if rl.regions.has_key(rpub["region"]):
          rpub_regions[rpub["_id"]]=rpub["region"]
    for doc in documents:
        if not doc["exclude"]:
            words=doc["clean_text"].strip().split()        
            for i in range(0,len(words)):
                for j in range(1,n+1):
                    if i+j > len(words) or (j > 2 and words[i+j-2] in delimiters):
                        break # don't span sentence ends
                    out_words=words[i:i+j]
                    if out_words[0]==question_end:
                       out_words[0]=sentence_end
                    if len(" ".join(out_words)) <= 240:
                      yield {'_id': {'region':rpub_regions[doc["region_pub"]],
                                    'ngram':" ".join(out_words),
                                    'n':j}, 
                            'k_groups': [0 if k==doc["k_group"] else 1 for k in range(0,k_folds)]}
                      if out_words[0]==sentence_end and j<n:
                          #pad sentence starts with the delimiter token
                          #in theory this needs to loop up to n, this is hardcoded for n=3 for simplicity
                          yield {'_id': {'region':rpub_regions[doc["region_pub"]],
                                         'ngram':sentence_end+" "+" ".join(out_words),
                                         'n':j+1},
                                 'k_groups': [0 if k==doc["k_group"] else 1 for k in range(0,k_folds)]}

  except:
    print >> sys.stderr, "Unexpected map error " 
    traceback.print_exc()
    raise


print >> sys.stderr, "Start Mapping"
BSONMapper(mapper)
print >> sys.stderr, "Done Mapping."
