from pymongo import MongoClient
import sys
conn=MongoClient("cdgmongoserver.chickenkiller.com", 27017)
db=conn.dialect_db
db.confusion_threshold.rename("confusion_threshold_"+sys.argv[1])
