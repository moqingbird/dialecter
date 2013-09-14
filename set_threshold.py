from pymongo import MongoClient
from MongoConnection import MongoConnection
import sys

db=MongoConnection().get().dialect_db
db.parameters.update({"name":"classification_threshold"}, {"$set":{"value" :float(sys.argv[1])/100}})
