from Region import Region
import pymongo
import sys
from pymongo import MongoClient

class RegionList:
    regions={}

    def populate(self,get_ngrams,check_exclude=False):
        connection=MongoClient('cdgmongoserver.chickenkiller.com', 27017)
        db=connection.dialect_db
        region_cur=db.regions.find()#{"$or":[{"_id":"ABN"},{"_id":"NI"},{"_id":"MANC"},{"_id":"BRIS"}]})
        regions=[region for region in region_cur]#region_cur[:]
        i=0
        for region in regions:
           if not check_exclude or region["exclude"]==False:
              try:
                  ngram_counts=region["word_counts"]
              except KeyError:
                  ngram_counts=None
              self.regions[region["_id"]]=Region(region["_id"],region["name"],ngram_counts,i)
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


