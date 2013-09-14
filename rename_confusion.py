from pymongo import MongoClient
from MongoConnection import MongoConnection
import sys
db=MongoConnection().get().dialect_db
db.confusion_threshold.rename("confusion_threshold_"+sys.argv[1])
