import sys
import pymongo
import math
from Region import Region
from pymongo import MongoClient

print("start")
connection=MongoClient('cdgmongoserver.chickenkiller.com', 27017)
db=connection.dialect_db
region_cur=db.regions.find()#{"$or":[{"_id":"ABN"},{"_id":"NI"},{"_id":"MANC"},{"_id":"BRIS"}]})
regions=[region for region in region_cur]#region_cur[:]
for region in regions:
       try:
           ngram_counts=region["word_counts"]
       except KeyError:
           ngram_counts=None
       print(region["_id"])
       r=Region(region["_id"],region["name"],ngram_counts,-1)
       r.calcLikelihoods(10, 1, 0.75)
print("done")
