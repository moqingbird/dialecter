import pymongo
import math
from NGram import NGram
from pymongo import MongoClient

class Region:
    def __init__(self,id,name,counts,seq=0):
        self.id=id
        self.name=name
        self.counts=counts
        self.ngrams={}
        self.sortedKeys=[]
        self.k=10
        self.startsWith={}
        self.seq=seq

    def populateNgrams(self):        
        connection=MongoClient('192.168.153.128', 27017)
        db=connection.dialect_db
        ngram_cur=db.region_ngrams.find({"_id.region":self.id},timeout=False)
        ngrams=[ngram for ngram in ngram_cur]
        for ngram in ngrams:
            self.ngrams[ngram["_id"]["ngram"]]=NGram(ngram["_id"]["ngram"],ngram["n"],ngram["totals"],ngram["likelihoods"],True)
            if ngram["n"] > 1:
                try:
                    self.startsWith[ngram["_id"]["ngram"][:ngram["_id.ngram"].rfind(" ")]].append(NGram(ngram["_id"]["ngram"],ngram["n"],ngram["total"],0,False))
                except KeyError:
                    self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]]=[]
                    self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]].append(NGram(ngram["_id"]["ngram"],ngram["n"],ngram["totals"],0,False))
            else:
                self.counts=[self.counts[i]+ngram["totals"][i] for i in range(0,self.k)]

    def getCount(self,k):
        return self.counts[k]

    def getNgrams(self):
        return self.ngrams

    def discount(self,ngram, words, count, totalCount,discount,k):
        try:
            if words==1:
                return (float(count)-discount)/float(totalCount)# for i in range(0,self.k)]
            else:
                return (float(count)-discount)/float(self.ngrams[ngram[:ngram.rfind(" ")]].counts[k])
            #[(float(ngram.counts[i])-discount)/float(self.ngrams[ngram.id[:ngram.id.rfind(" ")]].counts[i]) for i in range(0,self.k)]
        except ZeroDivisionError:
            print("Zero divide error. region: %s, ngram: %s, words: %d, count: %d, totalCount: %d, k: %d" % (self.id,ngram,words,count,totalCount,k))
            raise

    def calcLikelihoods(self,witholdFraction,witholdSeq,discount):        
        connection=MongoClient('192.168.153.128', 27017)
        db=connection.dialect_db
        self.ngrams={}
        self.startsWith={}
        self.counts=[0 for i in range(0,self.k)]
        likelihood_defaults=[0 for i in range(0,self.k)]
        region_pub_cur=db.region_pubs.find({"region":self.id,"publication":"REDDIT"})    
        region_pubs=region_pub_cur[:]
        for region_pub in region_pubs:
            ngram_cur=db.rpub_ngrams.find({"_id.region_pub":region_pub["_id"]})
            ngrams=ngram_cur[:]
            for ngram in ngrams:    
                if ngram["_id"]["ngram"] in self.ngrams:
                    self.ngrams[ngram["_id"]["ngram"]].counts=[self.ngrams[ngram["_id"]["ngram"]].counts[i]+ngram["totals"][i] for i in range(0,self.k)]
                else:
                    self.ngrams[ngram["_id"]["ngram"]]=NGram(ngram["_id"]["ngram"],ngram["_id"]["n"],ngram["totals"],likelihood_defaults,False)
                    if ngram["_id"]["n"] > 1:
                        try:
                            self.startsWith[ngram["_id"]["ngram"][:ngram["_id.ngram"].rfind(" ")]].append(NGram(ngram["_id"]["ngram"],ngram["_id"]["n"],ngram["total"],0,False))
                        except KeyError:
                            self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]]=[]
                            self.startsWith[ngram["_id"]["ngram"][:ngram["_id"]["ngram"].rfind(" ")]].append(NGram(ngram["_id"]["ngram"],ngram["_id"]["n"],ngram["totals"],0,False))
                    else:
                        self.counts=[self.counts[i]+ngram["totals"][i] for i in range(0,self.k)]

        db.region_ngrams.remove({"region":self.id})
        db.regions.save({"_id":self.id,
                         "name":self.name,
                         "word_counts":self.counts})

        for ngram in sorted(self.ngrams.iterkeys()):
#            tmp=self.discount(self.ngrams[ngram],self.counts,discount)
#            for i in range(0,self.k):
#                tmp2=self.discount(self.ngrams[ngram],self.counts,discount)
#                tmp3=math.log(tmp2[i])
            
            tmp=0
            self.ngrams[ngram].likelihoods=[0 if self.ngrams[ngram].counts[i] == 0 
                                            else math.log(self.discount(self.ngrams[ngram].id, self.ngrams[ngram].words, self.ngrams[ngram].counts[i],self.counts[i],discount,i)) for i in range(0,self.k)]
            #self.ngrams[ngram].likelihoods=[0 if self.ngrams[ngram].counts[i] == 0 else math.log(self.discount(self.ngrams[ngram],self.counts,discount)[i]) for i in range(0,self.k)]
            db.region_ngrams.save({"_id": {"region":self.id,
                                           "ngram":ngram},
                                   "n":self.ngrams[ngram].words,
                                   "totals":self.ngrams[ngram].counts,
                                   "likelihoods":self.ngrams[ngram].likelihoods})  
    
    def getSortedKeys(self):
        return self.sortedKeys

    def getStartsWith(self,start):
        try:
            return self.startsWith[start]
        except KeyError:
            return [NGram("",0,0,0,False)]

    def getLikelihood(self,ngram):
        n=self.ngrams.get(ngram)
        return n.likelihood


