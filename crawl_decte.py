import PubCrawler
from PubCrawler import *
from PubGroup import PubGroup
from pymongo import MongoClient

from RegionList import RegionList
from crawl_functions import decte_crawler

connection=MongoClient('cdgmongoserver.chickenkiller.com',27017);
db=connection.dialect_db
pub=db.publications.find_one({"_id": "DECTE"})
pubgroup = PubGroup(pub["_id"],pub["name"],pub["url"],200,connection)

crawler=PubCrawler(None,"NEWC",pubgroup.baseurl,pubgroup,connection,"DECTE_TEST",decte_crawler)
crawler.set_auth("decte","G3ordie")
crawler.crawl(pubgroup.baseurl,0)
crawler.save()
print("done")
