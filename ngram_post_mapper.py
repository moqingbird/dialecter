#!/usr/bin/env python

import sys
import traceback
sys.path.append(".")

from pymongo_hadoop import BSONMapper

def mapper(documents):
  try:
    delimiter="[[$$$]]"
    n=3
    k_folds=10
    for doc in documents:
        if not doc["exclude"]:
            words=doc["clean_text"].strip().split()        
            for i in range(0,len(words)):#-len(delimiter.split())):
                for j in range(1,n+1):
                    if i+j > len(words) or (j > 2 and words[i+j-2] == delimiter):
                        break # don't span sentence ends
                    yield {'_id': {'post': doc["_id"],
                                   'ngram':" ".join(words[i:i+j]),
                                   'n':j},
                           'count':1}
  except:
    print >> sys.stderr, "Unexpected map error " 
    traceback.print_exc()
    raise


print >> sys.stderr, "Start Mapping"
BSONMapper(mapper)
print >> sys.stderr, "Done Mapping."
