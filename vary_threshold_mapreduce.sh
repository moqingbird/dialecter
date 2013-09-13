#!/bin/bash
i=5
while [[ $i -lt 75 ]]
do
   echo $i
   python set_threshold.py $i
   hadoop jar /usr/mongo-hadoop/streaming/target/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper /home/ubuntu/dev/dialecter/reconfuse_mapper.py -reducer /home/ubuntu/dev/dialecter/reconfuse_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.results_g33 -outputURI mongodb://cdgmongoserver.chickenkiller.com/dialect_db.confusion_threshold  
   python rename_confusion.py $i
   i=$(($i+5))
done
