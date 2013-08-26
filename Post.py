import math
import pymongo
import gc
from pymongo import MongoClient
from datetime import datetime

import sys

def timeme(msg):
    None
    #print >> sys.stderr, msg + " - " +str(datetime.now())

class Post:
    def __init__(self,id,regionId,content,discount,testMode):
        self.id=id
        self.regionId=regionId
        self.likelihood1=1
        self.likelihood2=1
        self.content=content
        self.testMode=testMode
        self.regionLikelihoods={}
        self.maxRegion=None
        self.maxLikelihood=None
        self.discount=discount
        self.k_group=-1


    def __calcAlpha__(self,region,prevWords):
        #timeme("sum slice")
        starts_with=region.getStartsWith(prevWords)
        if starts_with==None:
            beta=1
        else:
            beta=1-sum([region.getLikelihood(i, self.k_group) for i in starts_with])
        starts_with=region.getStartsWith(prevWords[prevWords.find(" ")+1:])
        if starts_with==None:
           normalise=1
        else:
           normalise=1-sum([region.getLikelihood(i, self.k_group) for i in starts_with])
        return beta/normalise

    def __estLikelihood__(self,ngram,region,words):
        likelihood=0
        try:
            timeme("  get")
            likelihood=region.getLikelihood(ngram, self.k_group)
            timeme("  got")
        except AttributeError:
            if words == 1:
              try:
                timeme("  1 gram calc") 
                likelihood=math.log((1.0-self.discount)/float(region.getCount(self.k_group)))
                timeme("  1 gram done")
              except ZeroDivisionError:
                print >> sys.stderr, "post: "+self.id+", region: " +region.id+", k: "+ str(self.k_group)
                raise
            else:
                timeme("   est -1")
                el=self.__estLikelihood__(ngram[ngram.find(" ")+1:],region,words-1)
                timeme("   set est")
                likelihood=self.__calcAlpha__(region,ngram[:ngram.rfind(" ")]) * el
                timeme("   post set")
        #timeme("   estLikelihood return")
        return likelihood
       
    def set_kgroup(self, k):
        self.k_group = k 

    def calc(self,db,rl,n,debug_mode=False):       
        timeme("get ngrams post: " + self.id + ", n: "+str(n))
        post_ngram_cur=db.post_ngrams.find({"_id.post":self.id, "_id.n":n})
        post_ngrams=[ngram["_id"]["ngram"] for ngram in post_ngram_cur]
        timeme("got ngrams")
        for r in rl.getKeys():
            self.regionLikelihoods[r]=0
        timeme("init regionLikelihoods")
        header=""
        outrows=[]
        for ngram in post_ngrams:
            header+=","+ngram
            timeme(ngram)
            for r in rl.getKeys():
                timeme("  likelihood for r " + str(r))
                tmp=self.__estLikelihood__(ngram,rl.get(r),n)
                if debug_mode:
                  outrows.append(r+","+str(tmp))
                self.regionLikelihoods[r]=self.regionLikelihoods[r]+tmp
                timeme("  post likelihood")
        timeme("done ngrams")
        if debug_mode:
           outfile=open(self.id+"_dbg.csv")
           outfile.write(header+"\n")
           for i in range(len(outrows)):
             outfile.write(outrows[i]+"\n")
           outfile.close()

        if not self.testMode:
            for rn in self.regionLikelihoods.keys():
                c.execute("insert into post_region (p_id, r_id, likelihood) values (%s,%s,%s)",(self.id, rn,self.regionLikelihoods[rn]));
        else:
            timeme("get max")
            for l in self.regionLikelihoods.keys():
                #print >> sys.stderr, self.maxRegion
                #print >> sys.stderr, str(self.maxLikelihood)
                #print >> sys.stderr, l
                #print >> sys.stderr, str(self.regionLikelihoods[l])  
                if self.regionLikelihoods[l] != 0 and (self.maxLikelihood==None or self.regionLikelihoods[l] > self.maxLikelihood):
                    self.maxLikelihood=self.regionLikelihoods[l]
                    self.maxRegion=l
        if self.maxRegion==None:
            self.maxRegion="None"
        timeme("maxRegion: "+self.maxRegion)
