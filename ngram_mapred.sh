hadoop jar /usr/local/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/hduser/dialecter/ngram_mapper.py -reducer /home/hduser/dialecter/ngram_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://127.0.0.1/dialect_db.posts -outputURI mongodb://127.0.0.1/dialect_db.rpub_ngrams  -numReduceTasks 1
