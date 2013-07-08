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

pubgroups={}

class PubUrlOpener(urllib.FancyURLopener):
   version="MoqBot;mailto:cdg.msc@gmail.com" 



class TextItem:

    def __init__(self,publication,id,author,content,saved):
        self.publication=publication
        self.id=id
        self.author=author
        self.content=content
        self.saved=saved

class PubCrawler:
    
    htmlCodes = { '&amp;':'&','&lt;':'<', '&gt;':'>','&quot;':'"', '&#39;':"'"}

    def __init__(self,id,region,url,pubgroup,dbconnection):
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
        self.connection=dbconnection
        #dbconnection=MongoClient('192.168.153.128',27017)   
        db=dbconnection.dialect_db
        tmp=db.posts.find({"publication":id})
        for t in tmp:
            self.textitems[t["_id"]]=(TextItem(self.id,t["_id"],"","",True))

    def crawl(self,url,level):
        if self.pubgroup.allowed(url):
            while self.pubgroup.lastcrawl + self.pubgroup.crawldelay > datetime.now():
                None
            opener=PubUrlOpener()
            self.pubgroup.setLastCrawl(datetime.now())
            fullUrl=url
            try:
                pagedoc=BeautifulSoup(''.join(opener.open(fullUrl).read()))
                items=pagedoc.findAll("item")
                pubDate=self.maxdate
                lastLink=""
                if len(items) == 0:
                    self.exit=True
                for item in items:
                    link=unicode(item.findAll("guid")[0].contents[0]).strip("/")
                    try:
                        pubDate=item.findAll("pubdate")[0].string
                        pubDate=datetime.strptime(pubDate[0:len(pubDate)-6],self.timeformat)
                        lastLink=link[link.find("comments/")+9:link.find("/",link.find("comments/")+9)]
                        if not url.upper().startswith(link.upper()):
                          self.crawl(link+"/.rss?sort=new",level+1)
                    except IndexError:
                        title=str(item.findAll("title")[0].contents[0])
                        author=title[0:title.find(" on ")].strip()
                        if not self.pubgroup.authors.has_key(author):
                            self.pubgroup.authors[author]=Author(author,False,null,null)
                        content=str(item.findAll("description")[0].contents[0])
                        content=content.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#39;',"'");
                        if self.textitems.has_key(link) and self.textitems.get(link).saved:
                            self.exit=True
                        if not self.textitems.has_key(link):
                            self.textitems[link]=(TextItem(id,link,author,content,False))
                            self.articles=self.articles+1
            except UnicodeError:
                print ("Unicode error on " + fullUrl)  
        if level==0:
            if self.articles < self.maxarticles and lastLink != "":
                newUrl=url
                if newUrl.find("&after=t3") >= 0:
                    newUrl=newUrl[0:newUrl.find("&after")]
                self.crawl(newUrl+"&after=t3_"+lastLink,level)

    def save(self):        
        #connection = MongoClient('192.168.153.128',27017)
        db=self.dbconnection.dialect_db
        for k in self.pubgroup.authors.iterkeys():
            if not self.pubgroup.authors[k].saved:
                db.authors.save({"_id":k,"pubgroup":self.pubgroup.id})
                self.pubgroup.authors[k].saved=True
        try:
            for key in self.textitems:
                numItems=len(self.textitems)
                if not self.textitems[key].saved:
                    db.posts.save({"_id":self.textitems[key].id,"publication":self.id,"author":self.textitems[key].author,"content":self.textitems[key].content})
        except: 
                e = sys.exc_info()[1]
                print( "Error: %s" % e )
                print(self.name)
                print(textitem.id)
                print(textitem.content[0:220])

def main() :
    connection=MongoClient('192.168.153.128',27017);
    db=connection.dialect_db
    cursor=db.publications.find()
    pubCur=cursor[:]
    for pub in pubCur:
        pubgroups[pub["_id"]] = PubGroup(pub["_id"],pub["name"],pub["url"],1000,connection)
        if pub["read_robots"]:
            pubgroups[pub["_id"]].readrobots()
        regionPubCur=db.region_pubs.find()
        for regionPub in regionPubCur:
            pubcrawler = PubCrawler(regionPub["_id"], regionPub["region"], regionPub["_id"], pubgroups[pub["_id"]], connection)
            url=pub["url"]+regionPub["_id"]+"/.rss?sort=new"
            pubcrawler.crawl(url,0)
            pubcrawler.save()
            
    print("done")
    var = input()

if __name__ == "__main__":
    main()