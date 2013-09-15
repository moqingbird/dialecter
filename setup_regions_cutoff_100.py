import pymongo
from MongoConnection import MongoConnection

db=MongoConnection().get().dialect_db
db.region_pubs.update({},{"$set": {"exclude": True}},multi=True)
rpubs=db.posts.aggregate([{"$match":{"exclude":False}},{"$group": {"_id":"$region_pub", "count":{"$sum":1}}}, {"$match": {"count": {"$gt":100}}},{"$project":{"_id":1}}])["result"]
for rpub in rpubs:
  res=db.region_pubs.update({"_id": rpub["_id"]},{"$set":{"exclude":False}})
rpubs=db.region_pubs.find({"$or": [{"_id":"/r/ireland"},{"_id":"/r/scotland"},{"_id":"/r/southwales"},{"_id":"/r/wales"}]})
for rpub in rpubs:
  res=db.region_pubs.update({"_id":rpub["_id"]},{"$set":{"exclude":True}})

db.regions.update({},{"$set": {"exclude": True, "calc_level":False}},multi=True)
rpub_cur=db.region_pubs.find({"exclude":False})
for rpub in rpub_cur:
   res=db.regions.update({"_id":rpub["region"]},{"$set":{"exclude":False}})

regions={}
region_cur=db.regions.find({"exclude":False})
for region in region_cur:
   regions[region["_id"]]=1
region_cur=db.regions.find({"exclude":False})
for region in region_cur:
   if not region.has_key("parent_id") or not regions.has_key(region["parent_id"]):
      res=db.regions.update({"_id":region["_id"]},{"$set":{"calc_level":True}})

