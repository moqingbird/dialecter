#!/bin/bash
db_name="localhost"
db_string=`cat mongoserver.config`
db_name=`echo $db_string | cut -d":" -f 1`

hadoop jar /usr/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/ubuntu/dev/dialecter/reconfuse_mapper.py -reducer /home/ubuntu/dev/dialecter/reconfuse_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://$db_name/dialect_db.results_g33 -outputURI mongodb://$db_name/dialect_db.confusion_threshold  
