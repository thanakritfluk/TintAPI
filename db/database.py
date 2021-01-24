import pymongo
from dotenv import load_dotenv 
import os

class DB(object):

    @staticmethod
    def init():
        load_dotenv()
        DB.DATABASE = ""
        try:
            client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
            client.server_info()
            DB.DATABASE = client['Tints']
        except :
            print("Error - Cannot connect to DB")
        
    @staticmethod
    def insert(collection, data):
       result = DB.DATABASE[collection].insert(data)
       return result
    
    def distint_lipstick():
       result = DB.DATABASE["Lipstick"].find({}).distinct("brand")
       return result
