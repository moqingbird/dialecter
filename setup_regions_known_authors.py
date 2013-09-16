import pymongo
from MongoConnection import MongoConnection
from Region import Region

db=MongoConnection().get().dialect_db
db.regions.update({},{"$set":{"exclude":True,"calc_level":False}},multi=True)
db.region_pubs.update({},{"$set":{"exclude":True}},multi=True)
db.regions.update({"_id": {"$in": ["ABN","BRUM","CAR","COR","DORS","GLAS","HARR","LEED","LEIC","MANX","NI","OXF","READ","SHROP","SURY","YRK"]}}, 
                  {"$set": {"exclude":False,"calc_level":True}},multi=True)
regions=db.regions.find({"exclude":False})
for region in regions:
  children=[region["_id"]]
  Region.getChildren(region["_id"],children, db)
  for c in children:
    res=db.region_pubs.update({"region":c},{"$set":{"exclude":False}})
