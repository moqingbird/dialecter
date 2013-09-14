from pymongo import MongoClient
import config

class MongoConnection:
   def __init__(self):
     server="localhost"
     port=27017
     try:
       infile=open(config.src_path+"mongoserver.config")
       fields=infile.read().split(":")
       server=fields[0]
       port=int(fields[1])
     except IOError:
       raise#None
     self.conn=MongoClient(server,port)

   def get(self):
     return self.conn

