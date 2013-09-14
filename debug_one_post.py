import sys
from datetime import datetime
from pymongo import MongoClient
from Region import Region
from RegionList import RegionList
from Post import Post
from MongoConnection import MongoConnection

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
	  print >> sys.stderr, child
	  #rpub_cur=db.region_pubs.find({"exclude":False},{"_id":1,"region":1})
	  rpub_cur=db.region_pubs.find({"region":child},{"_id":1,"region":1})
	  for rpub in rpub_cur:
		#if rl.regions.has_key(rpub["region"]):
		  rpub_regions[rpub["_id"]]=rpub["region"]
doc=db.posts.find_one({"_id":sys.argv[1]})
post=Post(doc["_id"],rpub_regions[doc["region_pub"]], doc["clean_text"],0.75,True)
post.set_kgroup(doc["k_group"])
print >> sys.stderr, str(datetime.now()) + doc["_id"]
post.calc(db,rl,n,True)

