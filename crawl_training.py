from PubCrawler import PubCrawler
from PubGroup import PubGroup
from pymongo import MongoClient

from RegionList import RegionList
from MongoConnection import MongoConnection
from crawl_functions import *

db=MongoConnection().get().dialect_db
cursor=db.publications.find()
pubCur=cursor[:]
for pub in pubCur:
     pubgroups[pub["_id"]] = PubGroup(pub["_id"],pub["name"],pub["url"],1000,connection)
     if pub["read_robots"]:
         pubgroups[pub["_id"]].readrobots()
     regionPubCur=db.region_pubs.find({"publication":pub["_id"]})
     for regionPub in regionPubCur:
         print("rpub: "+regionPub["_id"])
         pubcrawler = PubCrawler(regionPub["_id"], regionPub["region"], regionPub["_id"], pubgroups[pub["_id"]], connection,"REDDIT_REGION_TRAIN",reddit_region_crawler)
         url=pub["url"]+regionPub["_id"]+"/.rss?sort=new"
         pubcrawler.crawl(url,0)
         pubcrawler.save()

print("done")
