from PIL.Image import NONE
import pymongo
import os

class DB(object):

    @staticmethod
    def init():
        DB.DATABASE = ""
        try:
            client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
            client.server_info()
            DB.DATABASE = client['Tints']
        except :
            print("Error - Cannot connect to DB")

    @staticmethod
    def find(collection, filters = None, field = None ):
        if filter is None and field is None:
            result = DB.DATABASE[collection].find({})
        else:
            result = DB.DATABASE[collection].find(filters,field)
        return result

    @staticmethod
    def insert(collection, data):
       result = DB.DATABASE[collection].insert(data)
       return result

    @staticmethod
    def update(collection, filters = None, field = None):
        result = DB.DATABASE[collection].update(filters, field)
        return result


    @staticmethod
    def distinct(collection, field, field_distinct):
        result = DB.DATABASE[collection].find(field).distinct(field_distinct)
        return result
