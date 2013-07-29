#!/usr/bin/env python

import sys
import traceback
sys.path.append(".")

from pymongo_hadoop import BSONReducer

k=10

def reducer(key, values):
  _counts  = [0 for i in range(0,k)]
  _count = 0
  try:
    for v in values:
        _count += 1
    return {'_id': key,'total':  _count}
  except:
    print >> sys.stderr, "Unexpected reduce error " 
    traceback.print_exc()
    err_file=open("~\\dialecter\\reduce_err.txt","w")
    traceback.print_exception(sys.exc_info()[0],
                              sys.exc_info()[1],
                              sys.exc_info()[2],
                              limit=None,
                              file=err_file)
    err_file.close()
    raise

print >> sys.stderr, "Start Reduce"
BSONReducer(reducer)
print >> sys.stderr, "Done Reduce"
