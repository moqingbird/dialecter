#!/usr/bin/env python

import sys
import traceback
import pymongo
import re
sys.path.append(".")

from pymongo import MongoClient
from pymongo_hadoop import BSONMapper
from RegionList import RegionList
from MongoConnection import MongoConnection


sentence_end="[[$$$]]"
question_end="[[???]]"

def is_special(word):
   if word != sentence_end and word != question_end and re.match("\\[\\[.*\\]\\]",word):
      return True
   return False

def too_special(w):
   if is_special(w[0]):
     return True
   count_special=0
   for i in range(1,len(w)):
     if is_special(w[i]):
        count_special+=1
     if count_special > len(w)/2:
        return True
   return False

def mapper(documents):
  try:
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
    valid_authors={}
    auth_cur=db.authors.find({"pubgroup":"REDDIT","selfClassification": {"$nin": ["unknown","conflict","non_uk"]}})
    for auth in auth_cur:
      valid_authors[auth["_id"]]=auth["selfClassification"]

    for doc in documents:
        if not doc["exclude"] and valid_authors.has_key(doc["author"]):
            words=doc["clean_text"].strip().split()        
            for i in range(0,len(words)):
                for j in range(1,n+1):
                    if i+j > len(words) or (j > 2 and words[i+j-2] in delimiters):
                        break # don't span sentence ends
                    out_words=words[i:i+j]
                    if out_words[0]==question_end:
                       out_words[0]=sentence_end
                    if not too_special(out_words) and len((" ".join(out_words)).encode("utf-8")) <= 240:
                      yield {'_id': {'region':valid_authors[doc["author"]],
                                    'ngram':" ".join(out_words),
                                    'n':j}, 
                            'k_groups': [0 if k==doc["k_group"] else 1 for k in range(0,k_folds)]}
                      if out_words[0]==sentence_end and j<n:
                          #pad sentence starts with the delimiter token
                          #in theory this needs to loop up to n, this is hardcoded for n=3 for simplicity
                          yield {'_id': {'region':valid_authors[doc["author"]],
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
