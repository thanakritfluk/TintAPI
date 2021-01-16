import pymongo
from dotenv import load_dotenv 
import os

class DB(object):

    @staticmethod
    def init():
        load_dotenv() 
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
        DB.DATABASE = client['Tints']
    
    @staticmethod
    def insert(collection, data):
       result = DB.DATABASE[collection].insert(data)
       return result