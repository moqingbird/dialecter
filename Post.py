import math
import pymongo
from pymongo import MongoClient

def timeme(msg):
    None
    #print(msg + " - " +str(datetime.now()))

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


    def __calcBeta__(self,rl,prevWords):
        timeme("sum slice")
        t=rl.get(self.regionId).getStartsWith(prevWords)
        return (1-sum([i.likelihood for i in rl.get(self.regionId).getStartsWith(prevWords)]))/ \
               (1-sum([i.likelihood for i in rl.get(self.regionId).getStartsWith(prevWords[prevWords.find(" ")+1:])]))

    def __estLikelihood__(self,ngram,regionId,rl,words):
        likelihood=0
        try:
            likelihood=rl.get(regionId).getLikelihood(ngram)
        except AttributeError:
            if words == 1:
                likelihood=math.log((1.0-self.discount)/float(rl.get(regionId).getCount(self.k_group)))
            else:
                timeme("est -1")
                el=self.__estLikelihood__(ngram[ngram.find(" ")+1:],regionId,rl,words-1,self.k_group)
                timeme("set est")
                likelihood=self.__calcBeta__(rl,ngram[:ngram.rfind(" ")]) * el
                timeme("post set")
        timeme("estLikelihood return")
        return likelihood
       
    def set_kgroup(self, k):
        self.k_group = k 

    def calc(self,db,rl,n):       
        correct=0
        global eq
        wrong=0
        global r3Wrong

        post_ngram_cur=db.post_ngrams.find({"_id.post":self.id, "n":n})
        post_ngrams=[ngram["_id"]["ngram"] for ngram in post_ngram_cur]

        for r in rl.getKeys():
            self.regionLikelihoods[r]=0
        for ngram in post_ngrams:
            for r in rl.getKeys():
                timeme("likelihood for r " + str(r))
                self.regionLikelihoods[r]=self.regionLikelihoods[r]+self.__estLikelihood__(ngram,r,rl,n)
                timeme("post likelihood")
        if not self.testMode:
            for rn in self.regionLikelihoods.keys():
                c.execute("insert into post_region (p_id, r_id, likelihood) values (%s,%s,%s)",(self.id, rn,self.regionLikelihoods[rn]));
        else:
            for l in self.regionLikelihoods.keys():
                if self.maxLikelihood==None or self.regionLikelihoods[l] > self.maxLikelihood:
                    self.maxLikelihood=self.regionLikelihoods[l]
                    self.maxRegion=l
            if self.regionId == self.maxRegion:
                correct=correct+1
            else:
                wrong=wrong+1
