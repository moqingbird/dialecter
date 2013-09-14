import sys
import memcache
import pymongo
import config
import re

from datetime import datetime
from memcache import Client
from pymongo import MongoClient
from NGram import NGram
from MongoConnection import MongoConnection

def timeme(msg):
    None
    #print >> sys.stderr, msg + " - " +str(datetime.now())

class RegionNgramCache:
   NGRAM=1
   STARTS_WITH=2

   def __init__(self):
      self.db=MongoConnection().get().dialect_db
      self.servers=[]
      self.server_count=0
      server_file=open(config.src_path+"memcached_servers.config")
      for line in server_file:
        if not line.startswith("#"):
           self.servers.append(Client([line]))
           self.server_count+=1

   def set_value(self, region, type, key, value):
      if not (type==self.NGRAM or type==self.STARTS_WITH):
           raise Exception("Invalid cache key type. Valid values are RegionNgramCache.NGRAM, RegionNgramCache.STARTS_WITH")
      server=hash(region.id)%self.server_count
      full_key=(region.id+"."+str(type)+"."+key.replace(" ", "-")).encode("utf-8")
      result=self.servers[server].set(full_key, value, 0)
      if str(result)!="True":
         raise Exception("Unable to cache key %s" % (key))

   def get_value(self, region,type, key):
      timeme("get hash")
      server=hash(region.id)%self.server_count
      timeme("get full key")
      valid_key=re.sub("[ \t\r\n\x00-\xff]","-",key)
      full_key=(region.id+"."+str(type)+"."+valid_key).encode("utf-8")
      timeme("get value")
      value=self.servers[server].get(full_key)
      timeme("got value")
      if not value:
         value=None
         # Normally you'd do a DB lookup when you get a cache miss, but we're loading the full set and not expiring them. We expect
         # a lot of misses where ngrams don't exist for a region, and in these case the extra lookup is a wasted 2 seconds
      return value
