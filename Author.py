import pymongo
from pymongo import MongoClient

class Author:
    def __init__(self,id,saved,flairText,flairCSS,selfClassification,countClassification):
        self.id=id
        self.saved=saved
        self.flairText=flairText
        self.flairCSS=flairCSS
        self.countClassification=countClassification
        self.selfClassification=selfClassification


