import pymongo
import math
import sys
from NGram import NGram
from pymongo import MongoClient
from RegionNgramCache import RegionNgramCache

class Region:
    def __init__(self,id,name,counts,total_count,seq=0, use_cache=False):
        self.id=id
        self.name=name
        self.counts=counts
        self.total_count=total_count
        self.ngrams={}
        self.sortedKeys=[]
        self.k=10
        self.startsWith={}
        self.seq=seq
        self.use_cache=use_cache
        self.cache=None
        if use_cache:
          self.cache=RegionNgramCache()

    def populateNgrams(self):        
        connection=MongoClient('cdgmongoserver.chickenkiller.com', 27017)
        db=connection.dialect_db
        ngram_cur=db.region_ngrams.find({"_id.region":self.id},timeout=False)
        ngrams=[ngram for ngram in ngram_cur]
        for ngram in ngrams:
            try:
              word_counts=ngram["word_counts"]
            except KeyError:
              word_counts=[]
            try:
              total_count=ngram["total_count"]
            except KeyError:
              total_count=0
            try:
              likelihoods=ngram["likelihoods"]
            except KeyError:
              likelihoods=[]
            try:
              total_likelihood=ngram["total_likelihood"]
            except KeyError:
              total_likelihood=0 
            self.ngrams[ngram["_id"]["ngram"]]=NGram(ngram["_id"]["ngram"],ngram["n"],word_counts,total_count,likelihoods,total_likelihood,True)
            if ngram["n"] > 1:
                try:
                    self.startsWith[ngram["_id"]["ngram"][:ngram["_id.ngram"].rfind(" ")]].append(ngram["_id"]["ngram"])
                except KeyError:
                    self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]]=[]
                    self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]].append(ngram["_id"]["ngram"])
            else:
                self.counts=[self.counts[i]+ngram["totals"][i] for i in range(0,self.k)]
                self.total_count+=ngram["grand_total"]

    def clearNgrams(self):
        self.ngrams={}
        self.startsWith={}

    def getCount(self,k):
        if k==None:
          return self.total_count
        return self.counts[k]

    def getNgrams(self):
        return self.ngrams

    def discount(self,ngram, words, count, totalCount,discount,k):
        try:
            if words==1:
                return (float(count)-discount)/float(totalCount)
            elif k != None:
                return (float(count)-discount)/float(self.ngrams[ngram[:ngram.rfind(" ")]].counts[k])
            else:
                return (float(count)-discount)/float(self.ngrams[ngram[:ngram.rfind(" ")]].total_count)
        except ZeroDivisionError:
            print("Zero divide error. region: %s, ngram: %s, words: %d, count: %d, totalCount: %d, k: %d" % (self.id,ngram,words,count,totalCount,k))
            raise

    def calcLikelihoods(self,witholdFraction,witholdSeq,discount):        
        connection=MongoClient('cdgmongoserver.chickenkiller.com', 27017)
        db=connection.dialect_db
        #n=db.parameters.find_one({"name":"n"})["value"]
        self.ngrams={}
        self.startsWith={}
        self.counts=[0 for i in range(0,self.k)]
        self.total_count=0
        likelihood_defaults=[0 for i in range(0,self.k)]
        #region_pub_cur=db.region_pubs.find({"region":self.id,"publication":"REDDIT"})    
        #region_pubs=region_pub_cur[:]
        #for region_pub in region_pubs:
        if 1==1:
            ngram_cur=db.region_ngrams.find({"_id.region":self.id})
            ngrams=ngram_cur[:]
            for ngram in ngrams:    
                if ngram["_id"]["ngram"] in self.ngrams:
                    self.ngrams[ngram["_id"]["ngram"]].counts=[self.ngrams[ngram["_id"]["ngram"]].counts[i]+ngram["totals"][i] for i in range(0,self.k)]
                    self.ngrams[ngram["_id"]["ngram"]].total_count+=ngram["grand_total"]
                else:
                    self.ngrams[ngram["_id"]["ngram"]]=NGram(ngram["_id"]["ngram"],
                                                             ngram["n"],
                                                             ngram["totals"],
                                                             ngram["grand_total"],
                                                             likelihood_defaults,
                                                             0,
                                                             False)
                    if ngram["n"] > 1:
                        try:
                            self.startsWith[ngram["_id"]["ngram"][:ngram["_id.ngram"].rfind(" ")]].append(ngram["_id"]["ngram"])
                        except KeyError:
                            self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]]=[]
                            self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]].append(ngram["_id"]["ngram"])
                    else:
                        self.counts=[self.counts[i]+ngram["totals"][i] for i in range(0,self.k)]
                        self.total_count+=ngram["grand_total"]
            ngram_cur.close()
            ngrams=[]
        db.regions.update({"_id":self.id},
                          {"$set":{"word_counts":self.counts, 
                                   "total_count":self.total_count}})

        for ngram in sorted(self.ngrams.iterkeys()):
            self.ngrams[ngram].likelihoods=[0 if self.ngrams[ngram].counts[i] == 0 
                                            else math.log(self.discount(self.ngrams[ngram].id, 
                                                          self.ngrams[ngram].words,
                                                          self.ngrams[ngram].counts[i],
                                                          self.counts[i],
                                                          discount,
                                                          i)) for i in range(0,self.k)]
            self.ngrams[ngram].total_likelihood=math.log(self.discount(self.ngrams[ngram].id, 
                                                                       self.ngrams[ngram].words,
                                                                       self.ngrams[ngram].
                                                                       total_count,
                                                                       self.total_count,
                                                                       discount,
                                                                       None))
            db.region_ngrams.update({"_id": {"region":self.id,
                                             "ngram":ngram}},
                                     {"$set": {"likelihoods":self.ngrams[ngram].likelihoods,
                                               "total_likelihood":self.ngrams[ngram].total_likelihood}})  
    
    def getSortedKeys(self):
        return self.sortedKeys

    def getStartsWith(self,start):
        try:
          if self.use_cache:
             return self.cache.get_value(self, RegionNgramCache.STARTS_WITH, start)
          else:
            return self.startsWith[start]
        except KeyError:
            return []

    def getLikelihood(self,ngram,k):
      try:
        return_val=0
        if self.use_cache:
           n=self.cache.get_value(self, RegionNgramCache.NGRAM, ngram)
        else:
          n=self.ngrams.get(ngram)
        if n!=None:
          if k==None:
            return_val=n.total_likelihood
          return_val=n.likelihoods[k]
        else:
          return_val=0
        return return_val
      except IndexError:
        print >> sys.stderr, "r: "+self.id+", ngram: " + ngram+ ", k: "+str(k)
        raise
