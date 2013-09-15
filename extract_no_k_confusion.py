import pymongo
from pymongo import MongoClient
from RegionList import RegionList

from MongoConnection import MongoConnection

db=MongoConnection().get().dialect_db

rl=RegionList()
rl.populate(False, True)

out_file=open("confusion.csv", "w")
for i in range(0,len(rl.regions)):
  out_file.write(","+rl.getBySeq(i).id)
out_file.write("\n")

for i in range(0,len(rl.regions)):
     out_file.write(rl.getBySeq(i).id+",")
     try:
       totals=db.confusion.find_one({"_id.region":rl.getBySeq(i).id, "_id.k_group":None})["totals"]
       out_file.write(",".join(str(t) for t in totals))
     except TypeError:
       None
     out_file.write("\n")
out_file.close()


