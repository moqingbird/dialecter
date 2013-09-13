from pymongo import MongoClient
import sys

conn=MongoClient("cdgmongoserver.chickenkiller.com", 27017)
db=conn.dialect_db
db.parameters.update({"name":"classification_threshold"}, {"$set":{"value" :float(sys.argv[1])/100}})
