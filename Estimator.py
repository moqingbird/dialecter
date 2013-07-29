import pymongo
import math
from datetime import datetime
from RegionList import RegionList
from Post import Post
from pymongo import MongoClient

rl=RegionList()
results=[]


global correct
global eq
global r2Wrong
global r3Wrong
global confusion
confusion=[]
wrong=0
r3Wrong=0
correct=0
eq=0

def slicedict(d, s):
    idx=d.keys().index(s)
    return {k:v for k,v in d.iteritems() if k.startswith(s)}

def timeme(msg):
    None
    #print(msg + " - " +str(datetime.now()))
    
class TestResult:
    def __init__(self,region,id,l1,l2):
        self.region=region
        self.id=id
        self.l1=l1
        self.l2=l2

"""
class Region:
    def __init__(self,id,name,count):
        self.id=id
        self.name=name
        self.count=count
        self.ngrams={}

    def getNgrams(self):        
        db=MySQLdb.connect(host="localhost",user="catherine",
                          passwd="catherine",db="dialect_db")
        c=db.cursor()
        c.execute("select rn.ngram, rn.likelihood " +\
                  "from region_ngram rn " +\
                  #"join ngram n on n.ngram = rn.ngram " +\
                  #" and n.include " +\
                  "where rn.region_id = %s "
                  "  and length(replace(rn.ngram, ' ', '')) = length(rn.ngram) ",(self.id))
        temp=list(c.fetchall())    
        for t in temp:
            self.ngrams[t[0]]=t[1]

    def getCount(self):
        return self.count

    def getLikelihood(self,ngram):
        return self.ngrams.get(ngram)
"""
"""
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

    def __calcBeta__(self,prevWords):
        #timeme("calcbeta")
        #temp=slicedict(rl.get(self.regionId).getNgrams(),prevWords)
        #print([i for i in temp])
        #print([rl.get(self.regionId).getLikelihood(i) for i in slicedict(rl.get(self.regionId).getNgrams(),prevWords)])
        timeme("sum slice")
        t=rl.get(self.regionId).getStartsWith(prevWords)
        return (1-sum([i.likelihood for i in rl.get(self.regionId).getStartsWith(prevWords)]))/ \
               (1-sum([i.likelihood for i in rl.get(self.regionId).getStartsWith(prevWords[prevWords.find(" ")+1:])]))
#slicedict(rl.get(self.regionId).getNgrams(),prevWords)
#slicedict(rl.get(self.regionId).getNgrams(),prevWords[prevWords.find(" ")+1:]
#rl.get(self.regionId).getLikelihood(i) 

    def __estLikelihood__(self,ngram,regionId,words):
        likelihood=0
        try:
            likelihood=rl.get(regionId).getLikelihood(ngram)
        except AttributeError:
            if words == 1:
                likelihood=math.log((1.0-self.discount)/float(rl.get(regionId).getCount()))
            else:
                timeme("est -1")
                el=self.__estLikelihood__(ngram[ngram.find(" ")+1:],regionId,words-1)
                timeme("set est")
                likelihood=self.__calcBeta__(ngram[:ngram.rfind(" ")]) * el
                timeme("post set")
        timeme("estLikelihood return")
        return likelihood
        

    def calc(self,text,n):       
        global correct
        global eq
        global wrong
        global r3Wrong
        global confusion
        db=MySQLdb.connect(host="localhost",user="catherine",
                          passwd="catherine",db="dialect_db")
        c=db.cursor()
        c.execute("select pn.ngram, count " +\
                "from post_ngram pn " +\
                "where p_id = %s " +\
                "and pn.words=%s ",(self.id,words))
        postNgrams=list(c.fetchall())
        for r in rl.getKeys():
            self.regionLikelihoods[r]=0
        for ngram in postNgrams:
            for r in rl.getKeys():
                #try:
                timeme("likelihood for r " + str(r))
                self.regionLikelihoods[r]=self.regionLikelihoods[r]+self.__estLikelihood__(ngram[0],r,words)
                timeme("post likelihood")
                #(rl.get(r).getLikelihood(ngram[0])*ngram[1])
                #except KeyError:
                #    self.regionLikelihoods[r]=estLikelihood(ngram[0],r,ngram[1])
                    #self.regionLikelihoods[r]+(math.log(1/rl.get(r).getCount())*ngram[1])
                #except TypeError:
                #    self.regionLikelihoods[r]=self.regionLikelihoods[r]+(math.log(1/rl.get(r).getCount())*ngram[1])
                #except AttributeError:
                #    self.regionLikelihoods[r]=self.regionLikelihoods[r]+(math.log(1/rl.get(r).getCount())*ngram[1])
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
            confusion[self.regionId-1][self.maxRegion-1]=confusion[self.regionId-1][self.maxRegion-1]+1
        db.commit();
        c.close();
        db.close();
"""
def printConfusion(outfile):    
    for i in range(len(confusion)):
        outfile.write("," +rl.getBySeq(i).id)
    outfile.write("\n")
    for i in range(len(confusion)):
        print(",".join(str(item) for item in confusion[i]))
        print(rl.getBySeq(i))
        outfile.write(rl.getBySeq(i).id+","+",".join(str(item) for item in confusion[i]))
        outfile.write("\n")
    print("correct: "+str(correct)+", wrong: "+str(wrong))
    outfile.write("correct: "+str(correct)+", wrong: "+str(wrong) + "\n")

def populatePostCount(db):
    ngram_cur=db.rpub_ngrams.find({"_id.post":{"$exists":1}})
    ngrams=ngram_cur[:]
    for ngram in ngrams:
        db.post_ngrams.save({"_id":{"post":ngram["_id"]["post"],
                                    "ngram":ngram["_id"]["ngram"]},
                             "n":ngram["_id"]["n"],
                             "total":ngram["total"]})
def main() :    
    global confusion
    global correct
    global wrong
    rl.populate(True)
    #rl.calcAll(10,1,0.75)
 #   db=MySQLdb.connect(host="localhost",user="catherine",
 #                     passwd="catherine",db="dialect_db")
 #   c=db.cursor()

    #withold=5;
    
    connection=MongoClient("cdgmongoserver.chickenkiller.com",27017)
    db=connection.dialect_db
   # populatePostCount(db)
    
    rpubs=[]
    rpub_regions={}
    rpub_cur=db.region_pubs.find({},{"_id":1,"region":1})
    for rpub in rpub_cur:
        if rl.regions.has_key(rpub["region"]):
            rpubs.append(rpub["_id"])
            rpub_regions[rpub["_id"]]=rpub["region"]
    #rpubs=[rpub for rpub in rpub_cur]
    #for rpub in rpubs:
    #    rpub_regions[rpub["_id"]]=rpub["region"]
    #post_cur=db.posts.find({"k_group": 0,"$or":[{"publication":"/r/bradford"},{"publication":"/r/midlands"}]})
    #tmp_posts=[post for post in post_cur]
    
    """    c.execute("select po.id, pb.r_id,po.content " +\
              "from post po " + \
              "join publication pb on pb.id = po.pb_id "#+\
              #"where mod(po.id,%s) = 0 ",(withold)
              )   
    temp=list(c.fetchall())   
    words=3"""
    
    n=3
    outfile=open(str(n) + 'grams_'+str(datetime.now()).replace(":","") +'.csv','w')
    outfile.write("k,correct %\n")
    confusion=[ [ 0 for i in range(len(rl.regions)) ] for j in range(len(rl.regions)) ]
    correct=0
    wrong=0
    posts={}
    for rpub in rpubs:
        post_cur=db.posts.find({"k_group": 0,"publication": rpub})
        tmp_posts=[post for post in post_cur]
        for post in tmp_posts:
            posts[post["_id"]]=Post(post["_id"],rpub_regions[post["publication"]], post["clean_text"],0.75,True)
            posts[post["_id"]].calc(db,rl,confusion,n,0)
#        outfile.write("k: "+str(0)+"," + str(100*(float(correct)/float(correct+wrong)))+"\n")
    printConfusion(outfile)
    outfile.close()
    
    """
    for withold in range(5):
        for seq in range(withold+4):
            timeme("withold " + str(withold+4)+ ", seq: " + str(seq))
            rl.calcAll(withold+4,seq,0.75)
            confusion=[ [ 0 for i in range(len(rl.regions)) ] for j in range(len(rl.regions)) ]
            posts={}
            correct=0
            wrong=0
            for t in temp:
                if t[0]%(withold+4) == seq:
                    timeme("post: " + str(t[0]))
                    posts[t[0]]=Post(t[0],t[1],t[2], 0.75,True)
                    posts[t[0]].calc(words)
            print("withold: "+str(withold+4)+", seq: " + str(seq))
            outfile.write("withold: "+str(withold+4)+", seq: " + str(seq) + " - " + str(float(correct)/float(correct+wrong))+"\n")
            printConfusion(outfile)
    outfile.close()
    c.close()
    db.close()"""
    print("done")
    
if __name__ == "__main__":
    main()
