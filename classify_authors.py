import pymongo
from pymongo import MongoClient
import requests
import json
import time
from PubGroup import PubGroup
from Tree import Tree
from Tree import Node

def get_region_tree(dbconnection,tree,parent=None):
    region_cur=db.regions.find({"parent_id":parent})
    print(parent)
    for region in region_cur:
        tree.add_node(region["_id"],parent)
        tree=get_region_tree(dbconnection,tree,region["_id"])
    return tree
                        
connection=MongoClient('cdgmongoserver.chickenkiller.com',27017);
db=connection.dialect_db
pubgroup=PubGroup.load("REDDIT",connection)
pubgroup.loadAuthors()

region_pubs = {}
region_pub_cur=db.region_pubs.find()
for region_pub in region_pub_cur:
    region_pubs[region_pub["_id"]] = region_pub["region"]

region_tree=Tree()
region_tree=get_region_tree(connection,region_tree)

post_counts=db.posts.aggregate( [{"$group": {"_id": {"publication": "$publication", "author": "$author"}, "count": {"$sum": 1}}},
                      {"$sort": {"_id.author": 1, "count": -1}},
                      {"$project": {"_id": 0,
					             "author": "$_id.author",
					             "pub_count": {
								      "publication": "$_id.publication",
									  "count": "$count"
							         }
							     }
				      },
					  {"$group": {"_id": "$author",
					            "pub_counts": {
											 "$push": "$pub_count"
											}
						        }
					  },
					  {"$project": {
					              "_id": 0,
								  "author": "$_id",
								  "pub_counts": 1
								 }
					  }
                    ]
                   )["result"]
countfile=open("C:\\Users\\Catherine\\Documents\\Birkbeck\\Project\\post_counts.txt","w")
# classification rules:
#   1) if the author posts to a single forum, that's their classification
#   2) if posting to multiple, if one count > 2x the next highest, choose that
#       a) unless there is a dominant lower count which falls within the region of the highest - then choose that as more specific
#   3) If there isn't a clear leader, but several counts fall within the same larger region (e.g posts to Bournemouth and Poole - group up to Dorset)
#       a) if there is a dominant sub-region amongs these, choose it
#       b) otherwise choose the smallest applicable larger region in the hierarchy
#   4) unsure what to do in other cases
for post_count in post_counts:
    if len(post_count["pub_counts"]) == 1:
        pubgroup.authors[post_count["author"]].countClassification = region_pubs[post_count["pub_counts"][0]["publication"]]
    else:# post_count["pub_counts"][0]["count"] > 2*(post_count["pub_counts"][1]["count"]):
        max_depth=region_tree[region_pubs[post_count["pub_counts"][0]["publication"]]].depth
        result=region_pubs[post_count["pub_counts"][0]["publication"]]
        result_count=post_count["pub_counts"][0]["count"]
        for pub_count in post_count["pub_counts"]:
            #if region_tree.is_descendent_of(region_pubs[post_count["pub_counts"][0]["publication"]],region_pubs[pub_count["publication"]]):
                # still not quite right, but probably close enough for now. doesn't account for sum of later lower posts adding up to dominance
                # in an implied region e.g. 10 posts to Scotland, 4 each to Devon, Falmouth, Exeter should imply the correct assignment is SW England, 
                # but will leave them in Scotland
                if region_tree.is_descendent_of(result,region_pubs[pub_count["publication"]]) or\
                   pub_count["count"] > 2*result_count:
                     result=region_pubs[pub_count["publication"]]
                     result_count=region_pubs[pub_count["count"]]
                else:
                   result=region_tree.get_common_parent(result,region_pubs[pub_count["publication"]])
                   result_count+=pub_count["count"]
        pubgroup.authors[post_count["author"]].countClassification = result
    #else:
        countfile.write("\"%s\",\"%s\"" %(post_count["author"],pubgroup.authors[post_count["author"]].countClassification))
        for pub in post_count["pub_counts"]:
           countfile.write(",\"%s\",\"%d\"" % (pub["publication"],pub["count"]))
        countfile.write("\n")
countfile.close()

#s=requests.Session()
#s.headers.update({'User-Agent' : 'MoqBot'})
#for author in pubgroup.authors:
#    retries=0
#    sleepInterval=60
#    r=s.get('http://www.reddit.com/r/unitedkingdom/api/flairlist.json?name='+author)
#    while (r.status_code == 504 and  retries < 10):
#        time.sleep(sleepInterval)
#        r=s.get('http://www.reddit.com/r/unitedkingdom/api/flairlist.json?name='+author)
#        retries+=1
#        sleepInterval*=5
#    try:
#        j=json.loads(r.content)
#        pubgroup.authors[author].flairText=j["users"][0]["flair_text"]
#        pubgroup.authors[author].flairCSS=j["users"][0]["flair_css_class"]
#        db.authors.save({"_id":author,
#                         "pubgroup":pubgroup.id,
#                         "flairText":pubgroup.authors[author].flairText,
#                         "flairCSS":pubgroup.authors[author].flairCSS,
#                         "selfClassification":pubgroup.authors[author].selfClassification,
#                         "countClassification":pubgroup.authors[author].countClassification})
#    except ValueError as e:
#        print(e.errno + " " + e.strerror)
#flairList=db.authors.aggregate( [{"$group": {"_id": {"flairText": "$flairText", "flairCSS": "$flairCSS"}, "count": {"$sum": 1}}}])
#flairfile=open("C:\\Users\\Catherine\\Documents\\Birkbeck\\Project\\raw_flair.txt","w")
#for flair in flairList["result"]:
#    print("\"%s\",\"%s\"" % (flair["_id"]["flairText"],flair["_id"]["flairCSS"]))
#    filefile.write(("\"%s\",\"%s\"\n" % (flair["_id"]["flairText"],flair["_id"]["flairCSS"])).encode("utf8"))
#filefile.close()
print("done")
var = input()
