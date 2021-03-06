python ./populate_likelihoods.py

python ./load_ngram_cache.py

hadoop jar /usr/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/ubuntu/dev/dialecter/validate_mapper.py -reducer /home/ubuntu/dev/dialecter/validate_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.posts -outputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.confusion  -jobconf mongo.input.query= {"batch":"REDDIT_REGION_TRAIN"}
