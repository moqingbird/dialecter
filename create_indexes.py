from pymongo import MongoClient

conn=MongoClient("cdgmongoserver.chickenkiller.com",27017)
db=conn.dialect_db
db.post_ngrams.ensure_index("_id.post")
db.region_ngrams.ensure_index("_id.region")

