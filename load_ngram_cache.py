import pymongo
from pymongo import MongoClient
from Region import Region
from RegionList import RegionList
import RegionNgramCache
from RegionNgramCache import RegionNgramCache

connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
db=connection.dialect_db
region_cur=db.regions.find({"exclude":False})
regions=[region for region in region_cur]
region_cur.close()
cache=RegionNgramCache()
i=0
for region in regions:
  try:
     ngram_counts=region["word_counts"]
  except KeyError:
    ngram_counts=None
  r=Region(region["_id"],region["name"],ngram_counts,0, None, 0,i,True)
  if ngram_counts!=None:
     r.populateNgrams()
  i+=1
  for n in r.ngrams:
     cache.set_value(r, RegionNgramCache.NGRAM, r.ngrams[n].id, r.ngrams[n])
  for s in r.startsWith:
      cache.set_value(r, RegionNgramCache.STARTS_WITH, s, r.startsWith[s])
