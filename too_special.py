import re
from MongoConnection import MongoConnection

sentence_delimiter="[[$$$]]"
question_delimiter="[[???]]"

def is_special(word):
   if word != sentence_delimiter and word != question_delimiter and re.match("\\[\\[.*\\]\\]",word):
      return True
   return False

def too_special(words):
   w=words.split()
   if is_special(w[0]):
     return True
   count_special=0
   for i in range(1,len(w)):
     if is_special(w[i]):
        count_special+=1
     if count_special > len(w)/2:
        return True
   return False

db=MongoConnection().get().dialect_db
ngrams=db.region_ngrams.find()
for ngram in ngrams:
    if too_special(ngram["_id"]["ngram"]):
       db.region_ngrams.update({"_id":ngram["_id"]},{"$set": {"special":True}})
    else:
       db.region_ngrams.update({"_id.region":ngram["_id"]["region"],"_id.ngram":ngram["_id"]["ngram"]},{"$set": {"special":True}})
