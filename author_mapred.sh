#!/bin/bash
if [ $# -ne 2 ]
then
  echo ""
  echo "Usage: author_mapred.sh streaming_dir source_dir"
  echo "  'streaming_dir' is the fully qualified path where mongo-hadoop-streaming-assembly-1.0.1.jar can be found"
  echo "  'source_dir' should be the fully qualified path where validate_mapper.py and validate_reducer.py can be found"
  echo ""
  exit 1
else
  stream_dir=$1
  src_dir=$2
fi

db_name="localhost"
db_string=`cat mongoserver.config`
db_name=`echo $db_string | cut -d":" -f 1`

hadoop jar $stream_dir/mongo-hadoop-streaming-assembly-1.0.1.jar -mapper $src_dir/validate_mapper.py -reducer $src_dir/validate_reducer.py  -inputformat com.mongodb.hadoop.mapred.MongoInputFormat -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat -inputURI mongodb://$db_name/dialect_db.posts -outputURI mongodb://$db_name/dialect_db.auth_confusion  -jobconf mongo.input.query={\"batch\":\"REDDIT_USER_TEST\"}
