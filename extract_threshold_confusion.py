import pymongo
from pymongo import MongoClient
from RegionList import RegionList

from MongoConnection import MongoConnection

db=MongoConnection().get().dialect_db

rl=["NI","COR","BRIS","CORN","ABN","BRAD","BRGT","BRNM","BRUM","CANT","CAR","DUB","DUND","EDB","ESX","GAL","GLAS","HULL","LEED","LEIC","LINC","LVP","MANC","NEWC","NORW","NTHM","OXF","PORT","YORK","SHEF","SOUTH","STAN","SURY","UNKNOWN"]
     
outfile=open("confusion_threshold.csv","w")
for r in  range(len(rl)):
  outfile.write(","+rl[r])
outfile.write("\n")

for r in range(len(rl)):
   if rl[r] != "UNKNOWN":
     outfile.write(rl[r]+",")
     try:
       totals=db.confusion_threshold.find_one({"_id":rl[r]})["totals"]
       outfile.write(",".join(str(t) for t in totals))
     except TypeError:
       raise #None
     outfile.write("\n")
outfile.close()


