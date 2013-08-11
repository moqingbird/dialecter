import sys
from datetime import datetime

import traceback
import pymongo

from pymongo import MongoClient
from RegionList import RegionList
from Post import Post

rl=RegionList()
rl.populate(False, True, True)
connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
db=connection.dialect_db
n=int(db.parameters.find_one({"name":"n"},{"_id":0,"value":1})["value"])
k=int(db.parameters.find_one({"name":"k"},{"_id":0,"value":1})["value"])
rpub_regions={}
rpub_cur=db.region_pubs.find({"exclude":False},{"_id":1,"region":1})
for rpub in rpub_cur:
       if rl.regions.has_key(rpub["region"]):
           rpub_regions[rpub["_id"]]=rpub["region"]

count=0
doc=db.posts.find_one({"exclude":False})
post=Post(doc["_id"],rpub_regions[doc["region_pub"]], doc["clean_text"],0.75,True)
post.set_kgroup(doc["k_group"])
post.calc(db, rl,n)
post.regionLikelihoods
for rn in post.regionLikelihoods.keys():
    print("rn: " +rn + ", " +str(post.regionLikelihoods[rn]))
