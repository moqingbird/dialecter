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

db.regions.update({},{"$set": {"exclude": True}},multi=True)
rpub_cur=db.region_pubs.find({"exclude":False})
for rpub in rpub_cur:
   res=db.regions.update({"_id":rpub["region"]},{"$set":{"exclude":False}})
