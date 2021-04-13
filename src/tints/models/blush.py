import datetime
from src.tints.db.database import DB

COLLECTION_NAME = 'Blush'

class Blush(object):
    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price
        self.created_at = datetime.datetime.utcnow()

    def insert(self):
        return DB.insert(collection=COLLECTION_NAME, data=self.json())

    def get_all_blush():
        return list(DB.find(collection=COLLECTION_NAME, filters={}, field={"brand":1,"name":1,"price":1,"price_sign":1,"currency":1, "image_link":1, "product_link":1, "category": 1, "product_colors":1, "api_featured_image":1}))

    def get_blush_by_skin_type(skin_type_name):
        collection_name = "".join((skin_type_name,COLLECTION_NAME))
        return list(DB.find(collection=collection_name))

    def json(self):
        return {'name':self.name,'product_colors':self.color,'price':self.price, 'created_at':self.created_at}