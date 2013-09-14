import urllib
import re
import time
import sys
import math
import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from xml.dom import minidom
from BeautifulSoup import BeautifulSoup
from PubGroup import PubGroup
from Author import Author
from MongoConnection import MongoConnection
from crawl_functions import *

pubgroups={}

class PubUrlOpener(urllib.FancyURLopener):
    version="MoqBot;mailto:cdg.msc@gmail.com" 

    def __init__(self,username,password):
        self.username=username
        self.password=password
        urllib.FancyURLopener.__init__(self)

    def prompt_user_passwd(self,host,realm):
        return(self.username,self.password)

class TextItem:

    def __init__(self,publication,id,author,content,saved):
        self.publication=publication
        self.id=id
        self.author=author
        self.content=content
        self.saved=saved

class PubCrawler:
    
    htmlCodes = { '&amp;':'&','&lt;':'<', '&gt;':'>','&quot;':'"', '&#39;':"'"}

    def __init__(self,id,region,url,pubgroup,db,batch,crawl_fn):
        self.id=id
        self.region=region
        self.baseurl=url
        self.readrobots=False
        self.pubgroup=pubgroup
        self.textitems={}
        self.mindate=datetime(2011,12,01)
        self.maxdate=datetime(2012,1,1)
        self.maxarticles=1000
        self.articles=0   
        self.timeformat="%a, %d %b %Y %H:%M:%S"
        self.exit=False 
        self.db=db
        self.batch=batch
        self.crawl_fn=crawl_fn
        self.username=None
        self.password=None
        tmp=db.posts.find({"publication":id})
        for t in tmp:
            self.textitems[t["_id"]]=(TextItem(self.id,t["_id"],"","",True))

    def set_auth(self,username,password):
        self.username=username
        self.password=password

    def crawl(self,url,level):
        if self.pubgroup.allowed(url):
            print(url)
            while self.pubgroup.lastcrawl + self.pubgroup.crawldelay > datetime.now():
                None
            opener=PubUrlOpener(self.username,self.password)
            self.pubgroup.setLastCrawl(datetime.now())
            self.newUrl=""
            try:
                pagedoc=BeautifulSoup(''.join(opener.open(url).read()))
                self.crawl_fn(url,pagedoc,level,self)
            except UnicodeError:
                print ("Unicode error on " + url)  
        if level==0:
            if self.articles < self.maxarticles and self.newUrl != "":
                self.crawl(self.newUrl, level)

    def save(self):        
        for k in self.pubgroup.authors.iterkeys():
            if not self.pubgroup.authors[k].saved:
                self.db.authors.save({"_id":k,"pubgroup":self.pubgroup.id})
                self.pubgroup.authors[k].saved=True
        try:
            for key in self.textitems:
                numItems=len(self.textitems)
                if not self.textitems[key].saved:
                    if self.id != None:
                        region_pub=self.id
                    else:
                        region_pub=None
                    db.posts.save({"_id":self.textitems[key].id,
                                   "region_pub":region_pub,
                                   "author":self.textitems[key].author,
                                   "batch":self.batch,
                                   "content":self.textitems[key].content})
        except: 
                e = sys.exc_info()[1]
                print( "Error: %s" % e )
                print(self.name)
                print(textitem.id)
                print(textitem.content[0:220])

def main() :
    db=MongoConnection().get().dialect_db
    cursor=db.publications.find()
    pubCur=cursor[:]
    for pub in pubCur:
        pubgroups[pub["_id"]] = PubGroup(pub["_id"],pub["name"],pub["url"],1000,db)
        if pub["read_robots"]:
            pubgroups[pub["_id"]].readrobots()
        regionPubCur=db.region_pubs.find({"publication":pub["_id"]})
        for regionPub in regionPubCur:
            print("rpub: "+regionPub["_id"])
            pubcrawler = PubCrawler(regionPub["_id"], regionPub["region"], regionPub["_id"], pubgroups[pub["_id"]], db,"TRAIN",reddit_region_crawler)
            url=pub["url"]+regionPub["_id"]+"/.rss?sort=new"
            pubcrawler.crawl(url,0)
            pubcrawler.save()
            
    print("done")

if __name__ == "__main__":
    main()
