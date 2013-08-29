from PubCrawler import PubCrawler
from PubGroup import PubGroup
from pymongo import MongoClient

from RegionList import RegionList
from crawl_functions import *

connection=MongoClient('cdgmongoserver.chickenkiller.com',27017);
db=connection.dialect_db
pub=db.publications.find_one({"_id":"REDDIT"})
pubgroup = PubGroup(pub["_id"],pub["name"],pub["url"],200,connection)
pubgroup.loadAuthors()

rl=RegionList()
rl.populate(False,True,False)

rpub_regions={}
rpub_cur=db.region_pubs.find({},{"_id":1,"region":1})
for rpub in rpub_cur:
    if rl.regions.has_key(rpub["region"]):
        rpub_regions[rpub["_id"]]=rpub["region"]

region_authors=db.posts.aggregate([{"$group": {"_id": {"region_pub": "$region_pub", "author": "$author"}, "count": {"$sum": 1}}},
                            {"$sort": {"_id.region_pub": 1, "count": -1}},
                            {"$project": {"_id": 0,
					                    "region_pub": "$_id.region_pub",
					                    "author_count": {
								            "author": "$_id.author",
									        "count": "$count"
							                }
							            }
				            },
					        {"$group": {"_id": "$region_pub",
					                "author_counts": {
											        "$push": "$author_count"
											    }
						            }
					        },
					        {"$project": {
					                    "_id": 0,
								        "region_pub": "$_id",
								        "author_counts": 1
								        }
					        }
                        ]
                        )["result"]
for region in region_authors:
    if rpub_regions.has_key(region["region_pub"]): 
       crawler=PubCrawler.PubCrawler(None,rpub_regions[region["region_pub"]],pubgroup.baseurl,pubgroup,connection,"REDDIT_USER_TEST",reddit_user_crawler)
       authors=region["author_counts"][1:5]
       for author in authors:
          crawler.crawl(pubgroup.baseurl+"/user/"+author["author"]+".rss?sort=new",0)
          crawler.save()
