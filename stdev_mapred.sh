#!/bin/bash
db_name="localhost"
db_string=`cat mongoserver.config`
db_name=`echo $db_string | cut -d":" -f 1`

hadoop jar /usr/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/ubuntu/dev/dialecter/sumsq_mapper.py    -reducer /home/ubuntu/dev/dialecter/sumsq_reducer.py     -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://$db_name/dialect_db.region_ngrams -outputURI mongodb://$db_name/dialect_db.sum_squares
