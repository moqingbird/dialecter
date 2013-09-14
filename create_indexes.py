from pymongo import MongoClient
from MongoConnection import MongoConnection

db=MongoConnection().get().dialect_db
db.post_ngrams.ensure_index("_id.post")
db.region_ngrams.ensure_index("_id.region")

