# -*- coding: utf-8 -*-
import sys
import pymongo
import codecs
import re
import random
from pymongo import MongoClient
from MongoConnection import MongoConnection

def escape (instring):
    return re.sub("(?P<esc>[.\\\*+^?{}\[\]|()\$])","\\ \g<esc>",instring).replace("\\ ","\\")

def __main__(batch,test_split):
  url="(\\w+://)?(((\\w+(\\-\\w+)?\\.){2,}\\w+(\\-\\w+)?)|\\w+(\\-\\w+)?\\.(com|net|org|edu))(/?([!#$&\\-;\\=\\?\\[\\]_a-zA-Z0-9~]|%[0-9a-fA-F]{2}|.[^ ]))*"
  url_token="[[URL]]"
  email="\w+@(\w+.)*\w+"
  email_token="[[EMAIL]]"
  sentence_end="(\.|:|;|!|<p>|</p>|<br/>|###)+" 
  sentence_end_token=" [[$$$]] "
  question_end="(\?)+"
  question_end_token=" [[???]] "
  square_brackets="[\[\]]"
  other_punctuation="[,\\-\"\(\)\*/]" 
  currency="(\$|�|\?|�)\\[\\[NUMBER\\]\\]"#"($|�|�|�)\d+(\.\d*)?"
  currency_token="[[CURRENCY]]"
  number="\d+(\.\d*)?"# prefix with "(?P<start>^| )" to exclude numbers embedded in other text
  number_token="[[NUMBER]]" # prefix with \g<start> if adding the above
  amp_escape="(&(?P<amp>#\d{1,4}|\w{2,6});)"
  amp_token="[[AMP\g<amp>]]" # need to sub out all the &gt; &#205; etc before removing semi-colons. can reinstate later if needed
  emoticon=""
  emoticon_token=" [[EMOTICON]]" 
  min_words=10
  #
  efile=codecs.open("wikipedia_emoticons.csv",encoding="utf-8")
  for line in efile:
      tmp=line.replace("\r\n","")
      tmp=line.replace("\r","")
      tmp=line.replace("\n","")
      icon=re.sub("(?P<esc>[.\\\*+^?{}\[\]|()])","\\ \g<esc>",line.replace("\r\n","").strip())
      emoticon+=icon+"|"
  emoticon="[^\w]?("+emoticon.rstrip("|").replace("\\ ","\\")+")"
  db=MongoConnection().get().dialect_db
  if batch != None:
    cursor=db.posts.find({"batch":batch})
  else:
    cursor=db.posts.find()
  posts=cursor[:]
  for post in posts:
      exclude=False
      cleaned=""
      if post["content"] == "[deleted]":
          exclude=True
          word_count=0
          k_group=-1
      else:
          cleaned=post["content"]
          cleaned=re.sub(square_brackets," ",cleaned) #do this first, before we insert any in the special tokens
          cleaned=re.sub(url,url_token,cleaned)
          cleaned=re.sub(number,number_token,cleaned)
          cleaned=re.sub(currency,currency_token,cleaned)
          cleaned=re.sub(email,email_token,cleaned)
          cleaned=re.sub(emoticon,emoticon_token,cleaned)
          cleaned=re.sub(amp_escape,amp_token,cleaned) # must precent sentence_end otherwise we mis-handle the semicolons in these
          cleaned=re.sub(sentence_end,sentence_end_token,cleaned)
          cleaned=re.sub(question_end, question_end_token,cleaned)
          cleaned=re.sub(other_punctuation," ",cleaned)
          cleaned=cleaned.replace("\'","") #remove single-quotes separately from other punctuation to avoid inserting spaces for apostrophes
          cleaned=sentence_end_token.lstrip() + " " +cleaned + sentence_end_token
          cleaned=re.sub("(?P<emote>(\s*"+escape(emoticon_token)+")+)","\g<emote>"+sentence_end_token, cleaned)
          cleaned=re.sub("\s+", " ",cleaned).upper()
          cleaned=re.sub("("+escape(sentence_end_token.lstrip())+")+",sentence_end_token.lstrip(), cleaned)
          cleaned=re.sub("("+escape(question_end_token.lstrip())+")+",question_end_token.lstrip(), cleaned)
          cleaned=re.sub("("+escape(sentence_end_token.lstrip())+escape(question_end_token.lstrip())+")+",question_end_token.lstrip(), cleaned)
          cleaned=re.sub("("+escape(question_end_token.lstrip())+escape(sentence_end_token.lstrip())+")+",question_end_token.lstrip(), cleaned)
          word_count=len(re.sub(escape(sentence_end_token),"",cleaned).split())
          if word_count < min_words:
              exclude=True
              k_group=-1
          elif test_split:
              k_group=random.randint(0,9)
          else:
              k_group=None
      res=db.posts.update({"_id":post["_id"]},
                          {"$set": 
                             {"clean_text":cleaned,
                              "exclude":exclude,
                              "word_count":word_count,
                              "k_group":k_group}
                          })

if __name__ == "__main__":
    if len(sys.argv) > 1:
       batch=sys.argv[1]
    else:
       batch=None
    if len(sys.argv) > 2:
      test_split=sys.argv[2]
    else:
      test_split=False
    __main__(batch,test_split)
