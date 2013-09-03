import pymongo
from pymongo import MongoClient
from RegionList import RegionList

rl=RegionList()
rl.populate(False, True)
connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
db=connection.dialect_db
k=int(db.parameters.find_one({"name":"k"},{"_id":0,"value":1})["value"])

for k_group in range(0,k):
  out_file=open("confusion"+str(k_group)+".csv", "w")
  for i in range(0,len(rl.regions)):
    out_file.write(","+rl.getBySeq(i).id)
  out_file.write("\n")

  for i in range(0,len(rl.regions)):
     out_file.write(rl.getBySeq(i).id+",")
     try:
       totals=db.confusion.find_one({"_id.region":rl.getBySeq(i).id, "_id.k_group":k_group})["totals"]
       out_file.write(",".join(str(t) for t in totals))
     except TypeError:
       None
     out_file.write("\n")
  out_file.close()

outfile=open("confusion_summary.csv","w")	

for i in range(0,len(rl.regions)):
  for j in range(0,len(rl.regions)):
    outfile.write(","+rl.getBySeq(j).id)
  outfile.write("\n")

  c=db.confusion.aggregate([{"$match":{"_id.region":rl.getBySeq(i).id}},{"$group": {"_id": "$_id.region", "totals": {"$push": "$totals"}}}])["result"][0]
  totals=[sum(j) for j in zip(*c["totals"])]
  outfile.write(c["_id"]+","+",".join(str(t) for t in totals)+"\n\n")

outfile.close()
     

