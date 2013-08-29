import PubCrawler
from Author import Author

def html_clean(in_text):
   return in_text.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#39;',"'")

def reddit_crawler(url,pagedoc,level,pc,byUser):
    after_param="&after=t3_"
    if byUser:
      after_param="&after=t1_"
    items=pagedoc.findAll("item")
    lastLink=""
    if len(items) == 0:
        exit=True
    for item in items:
        link=unicode(item.findAll("guid")[0].contents[0]).strip("/")
        try:
            pubDate=item.findAll("pubdate")[0].string
            if not byUser:
              lastLink=link[link.find("comments/")+9:link.find("/",link.find("comments/")+9)]
            if not url.upper().startswith(link.upper()) and not byUser:
                pc.crawl(link+"/.rss?sort=new",level+1)
        except IndexError:
            title=str(item.findAll("title")[0].contents[0])
            author=title[0:title.find(" on ")].strip()
            if not pc.pubgroup.authors.has_key(author):
                pc.pubgroup.authors[author]=Author(author,False,None,None,None,None)
            content=str(item.findAll("description")[0].contents[0])
            content=html_clean(content)
            if pc.textitems.has_key(link) and pc.textitems.get(link).saved:
                exit=True
            if not pc.textitems.has_key(link):
                pc.textitems[link]=(PubCrawler.TextItem(id,link,author,content,False))
                pc.articles=pc.articles+1
            if byUser:
               lastLink=link[link.rfind("/")+1:]
    if lastLink != "":
        pc.newUrl=url
        if pc.newUrl.find(after_param) >= 0:
               pc.newUrl=pc.newUrl[0:pc.newUrl.find(after_param)]
        pc.newUrl=pc.newUrl+after_param+lastLink

def reddit_region_crawler(url,pagedoc,level,pc):
    reddit_crawler(url,pagedoc,level,pc,False)

def reddit_user_crawler(url, pagedoc,level,pc):
    reddit_crawler(url,pagedoc,level,pc,True)

def decte_crawler(url, pagedoc,level,pc):
    if not url.endswith(".xml"):
        items=pagedoc.findAll("a")
        for item in items:
            filename=item.get("href")
            if filename.find(".xml") >= 0 and filename != "decte.xml":
                newUrl=url[0:url.rfind("/")+1]+filename
                pc.crawl(newUrl,level+1)
    else:
        location=pagedoc.findAll("residence")[0].contents[0]   
        tmp=pagedoc.findAll("tei")
        title=pagedoc.findAll("tei")[0].get("xml:id")
        id=title+".xml"
        doc_authors=[]
        content={}
        authors=pagedoc.findAll("person")
        for author in authors:
            author_id=author.get("xml:id")
            if author_id.startswith("informant"):
                doc_authors.append(author_id)
                content[author_id]=""
                if not pc.pubgroup.authors.has_key(author_id):
                    pc.pubgroup.authors[author_id]=Author(author_id,False,None,None,None,None)
        items=pagedoc.findAll("u")
        if len(items) > 0:
            for item in items:
                if item.get("who").startswith("#informant"):     
                    content[item.get("who").strip("#")]+=item.contents[0]+"."
            for author in doc_authors:
              content[author]=html_clean(content[author])
              item_id=title+"_"+author
              if pc.textitems.has_key(item_id) and pc.textitems.get(item_id).saved:
                  exit=True
              if not pc.textitems.has_key(item_id):
                pc.textitems[item_id]=(PubCrawler.TextItem(None,item_id,author,content[author],False))
                pc.articles+=1

def twitter_crawler(url,pagedoc,level,pc):
    None
