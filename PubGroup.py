import pymongo
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from Author import Author

class PubGroup:
    def __init__(self,id,name,baseurl,requiredPosts,dbconnection):
        self.id=id
        self.baseurl=baseurl
        self.disallowed=[]
        self.authors={}
        self.crawldelay=timedelta(seconds=2)
        self.lastcrawl=datetime.now()   
        self.dbconnection=dbconnection
    
    @staticmethod
    def load(id,dbconnection):
        db=dbconnection.dialect_db
        result=db.publications.find_one({"_id":id})
        return PubGroup(result["_id"],result["name"],result["url"],0,dbconnection)

    def readrobots(self):
            print self.baseurl.find("//")
            robotlocation = self.baseurl+"/robots.txt"
            print robotlocation
            robotdoc = urllib.urlopen(robotlocation).read().upper()
            lines=[]
            startindex=0
            endindex=0
            useragent="MoqBot;mailto:cdg.msc@gmail.com" 
            if robotdoc.find("User-agent: "+useragent) < 0:
                startindex=robotdoc.find("USER-AGENT: *")+14
                endindex=len(robotdoc)
            else:
                startindex=robotdoc.find("USER-AGENT: "+useragent.upper())+19
                endindex=robotdoc.find("USER-AGENT",startindex)
            for line in robotdoc[startindex:endindex].split("\n"):
                if line.find("DISALLOW") >= 0:
                    self.disallowed.append(line[line.find("DISALLOW:")+10:].strip())
                elif line.find("CRAWL-DELAY") >= 0:
                    self.crawldelay=int(line.replace("CRAWL-DELAY:","").strip())
            print(self.disallowed)

    def setLastCrawl(self,lastcrawl):
        self.lastcrawl=lastcrawl

    def allowed(self,testurl):
        if testurl.find(self.baseurl) > 0:
            print "wrong publication group for url " + testurl
        else:
            testurl=testurl.replace(self.baseurl, "").upper()
            for path in self.disallowed:
                pattern=re.compile(path.replace("?", "\\?").replace('*', '[^/]*?'))
                if pattern.match(testurl): 
                    return False
        return True

    def loadAuthors(self):
        db=self.dbconnection.dialect_db
        authCur=db.authors.find({"pubgroup":self.id})
        for author in authCur:
            try:
                flairText=author["flairText"]
            except KeyError:
                flairText=""
            try:
                flairCSS=author["flairCSS"]
            except KeyError:
                flairCSS=""
            try:
                selfClassification=author["selfClassification"]
            except KeyError:
                selfClassification=""
            try:
                countClassification=author["countClassification"]
            except KeyError:
                countClassification=""
            a=Author(author["_id"],True,flairText,flairCSS,selfClassification,countClassification)
            self.authors[author["_id"]]=a

