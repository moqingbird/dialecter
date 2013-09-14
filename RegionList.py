from Region import Region
import pymongo
import sys
from pymongo import MongoClient
from MongoConnection import MongoConnection

class RegionList:
    def __init__(self):
      self.regions={}

    def populate(self,get_ngrams,check_exclude=False,use_cache=False):
        db=MongoConnection().get().dialect_db
        region_cur=db.regions.find()#{"$or":[{"_id":"ABN"},{"_id":"NI"},{"_id":"MANC"},{"_id":"BRIS"}]})
        regions=[region for region in region_cur]#region_cur[:]
        i=0
        for region in regions:
           try:
             exclude=region["exclude"]
           except KeyError:
             exclude=False
           if check_exclude==False or exclude==False:
              try:
                  ngram_counts=region["word_counts"]
              except KeyError:
                  ngram_counts=[]
              try:
                  total_count=region["total_count"]
              except KeyError:
                  total_count=None
              self.regions[region["_id"]]=Region(region["_id"],
                                                 region["name"],
                                                 ngram_counts,
                                                 total_count, 
                                                 i, 
                                                 use_cache)
              if ngram_counts!=None and get_ngrams == True:
                  self.regions[region["_id"]].populateNgrams()
              i+=1

    def get(self,index):
        return self.regions[index]

    def getKeys(self):
        return self.regions.keys();

    def getBySeq(self,seq):
        for region in self.regions.itervalues():
            if region.seq==seq:
                return region

    def calcAll(self,witholdFraction,witholdSeq,discount):
        for r in self.regions.keys():
            self.regions.get(r).calcLikelihoods(witholdFraction,witholdSeq,discount)


