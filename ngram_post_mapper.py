#!/usr/bin/env python

import sys
import traceback
sys.path.append(".")

from pymongo_hadoop import BSONMapper

def mapper(documents):
  try:
    sentence_end="[[$$$]]"
    question_end="[[???]]"
    delimiters=[sentence_end,question_end]

    n=3
    k_folds=10
    for doc in documents:
        if not doc["exclude"]:
            words=doc["clean_text"].strip().split()        
            for i in range(0,len(words)):#-len(delimiter.split())):
                for j in range(1,n+1):
                    if i+j > len(words) or (j > 2 and words[i+j-2] in delimiters):
                        break # don't span sentence ends
                    out_words=words[i:i+j]
                    if out_words[0]==question_end:
                       out_words[0]=sentence_end
                    yield {'_id': {'post': doc["_id"],
                                   'ngram':" ".join(out_words),
                                   'n':j},
                           'count':1}
                    if out_words[0]==sentence_end and j<n:
                       #pad sentence starts with the delimiter token
                       #in theory this needs to loop up to n, this is hardcoded for n=3 for simplicity
                       yield {'_id': {'post': doc["_id"],
                                      'ngram':sentence_end+" "+" ".join(out_words),
                                      'n':j+1},
                              'count':1}
  except:
    print >> sys.stderr, "Unexpected map error " 
    traceback.print_exc()
    raise


print >> sys.stderr, "Start Mapping"
BSONMapper(mapper)
print >> sys.stderr, "Done Mapping."
