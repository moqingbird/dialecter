hadoop jar /usr/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/ubuntu/dev/dialecter/ngram_region_mapper.py -reducer /home/ubuntu/dev/dialecter/ngram_region_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.posts -outputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.region_ngrams    -jobconf mongo.input.query={\"batch\":\"REDDIT_REGION_TRAIN\"}

hadoop jar /usr/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/ubuntu/dev/dialecter/ngram_post_mapper.py -reducer /home/ubuntu/dev/dialecter/ngram_post_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.posts -outputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.post_ngrams 

python ./create_indexes.py

python ./populate_likelihoods.py

python ./load_ngram_cache.py

hadoop jar /usr/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/ubuntu/dev/dialecter/validate_mapper.py -reducer /home/ubuntu/dev/dialecter/validate_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.posts -outputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.confusion  -jobconf mongo.input.query={\"batch\":\"REDDIT_REGION_TRAIN\"}
