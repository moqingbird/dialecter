import MySQLdb
import re
from Region import Region

class NGrammer:
    """description of class"""

def main() :
    updateRegions=False
    db=MySQLdb.connect(host="localhost",user="catherine",
                      passwd="catherine",db="dialect_db")
    c=db.cursor()
    c.execute("select p.id, p.content " +\
                "from post p " +\
                "where not exists (select 1 from post_ngram where p_id = p.id)")
    posts=list(c.fetchall())
    c.close()
    db.close()
    oneGrams={}
    twoGrams={}
    threeGrams={}
    for post in posts:
        words = re.sub("['.,\"\':;?\-!\[\]\(\)]","",post[1].upper()).split()
        for i in range(0,len(words)):
            try:
                oneGrams[words[i]]=oneGrams[words[i]]+1
            except KeyError:
                oneGrams[words[i]]=1
            if i < len(words)-1:
                try:
                    twoGrams[words[i]+" "+words[i+1]]=twoGrams[words[i]+" "+words[i+1]]+1
                except KeyError:
                    twoGrams[words[i]+" "+words[i+1]]=1
            if i < len(words)-2:
                try:
                    threeGrams[words[i]+" "+words[i+1]+" "+words[i+2]]=twoGrams[words[i]+" "+words[i+1]+" "+words[i+2]]+1
                except KeyError:
                    threeGrams[words[i]+" "+words[i+1]+" "+words[i+2]]=1
        db=MySQLdb.connect(host="localhost",user="catherine",
                      passwd="catherine",db="dialect_db")
        c=db.cursor()
        for item in oneGrams.keys():
            if oneGrams[item] > 0:
                c.execute("insert into post_ngram (ngram,p_id,words,count) " +\
                      "values(%s,%s,1,%s)",(item,post[0],oneGrams[item]))            
                oneGrams[item]=0
        for item in twoGrams.keys():
            if twoGrams[item] > 0:
                c.execute("insert into post_ngram (ngram,p_id,words,count) " +\
                      "values(%s,%s,2,%s)",(item,post[0],twoGrams[item]))         
                twoGrams[item]=0
        for item in threeGrams.keys():
            if threeGrams[item] > 0:
                c.execute("insert into post_ngram (ngram,p_id,words,count) " +\
                        " values (%s,%s,3,%s)",(item,post[0],threeGrams[item]))         
                threeGrams[item]=0
        db.commit()
        c.close()
        db.close()
    
#    if updateRegions:
#        db=MySQLdb.connect(host="localhost",user="catherine",
#                      passwd="catherine",db="dialect_db")
#        c=db.cursor()
#        for item in oneGrams.keys():
#            c.execute("insert into ngram (ngram) (select %s from dual where not exists (select 1 from ngram where ngram = %s))",(item,item))
#        for item in twoGrams.keys():
#            c.execute("insert into ngram (ngram) (select %s from dual where not exists (select 1 from ngram where ngram = %s))",(item,item))
#        for item in threeGrams.keys():
#            c.execute("insert into ngram (ngram) (select %s from dual where not exists (select 1 from ngram where ngram = %s))",(item,item))
#        db.commit()
#        c.close()
#        db.close()

if __name__ == "__main__":
    main()

