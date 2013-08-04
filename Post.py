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
        self.maxRegion=0
        self.maxLikelihood=None
        self.discount=discount
        self.k_group=-1


    def __calcBeta__(self,region,prevWords):
        timeme("sum slice")
        return (1-sum([region.getLikelihood(i, self.k_group) for i in region.getStartsWith(prevWords)]))/ \
               (1-sum([region.getLikelihood(i, self.k_group) for i in region.getStartsWith(prevWords[prevWords.find(" ")+1:])]))

    def __estLikelihood__(self,ngram,region,words):
        likelihood=0
        try:
            likelihood=region.getLikelihood(ngram, self.k_group)
        except AttributeError:
            if words == 1:
              try:
                likelihood=math.log((1.0-self.discount)/float(region.getCount(self.k_group)))
              except ZeroDivisionError:
                print >> sys.stderr, "post: "+self.id+", region: " +region.id+", k: "+ str(self.k_group)
                raise
            else:
                timeme("est -1")
                el=self.__estLikelihood__(ngram[ngram.find(" ")+1:],region,words-1)
                timeme("set est")
                likelihood=self.__calcBeta__(region,ngram[:ngram.rfind(" ")]) * el
                timeme("post set")
        timeme("estLikelihood return")
        return likelihood
       
    def set_kgroup(self, k):
        self.k_group = k 

    def calc(self,db,rl,n):       
        correct=0
        print("start calc")
        global eq
        wrong=0
        global r3Wrong

        timeme("get ngrams post: " + self.id + ", n: "+str(n))
        post_ngram_cur=db.post_ngrams.find({"_id.post":self.id, "_id.n":n})
        post_ngrams=[ngram["_id"]["ngram"] for ngram in post_ngram_cur]
        timeme("got ngrams")

        for r in rl.getKeys():
            self.regionLikelihoods[r]=0
        timeme("init regionLikelihoods")
        for r in rl.getKeys():
            region=rl.get(r)
            print(r)
            region.populateNgrams()
            for ngram in post_ngrams:
                self.regionLikelihoods[r]=self.regionLikelihoods[r]+self.__estLikelihood__(ngram,region,n)
            region.clearNgrams()
        #for ngram in post_ngrams:
        #    timeme(ngram)
        #    for r in rl.getKeys():
        #        timeme("likelihood for r " + str(r))
        #        self.regionLikelihoods[r]=self.regionLikelihoods[r]+self.__estLikelihood__(ngram,r,rl,n)
        #        timeme("post likelihood")
        timeme("done ngrams")
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
                if self.maxLikelihood==None or self.regionLikelihoods[l] > self.maxLikelihood:
                    self.maxLikelihood=self.regionLikelihoods[l]
                    self.maxRegion=l
            if self.regionId == self.maxRegion:
                correct=correct+1
            else:
                wrong=wrong+1
        timeme("maxRegion: "+self.maxRegion)
