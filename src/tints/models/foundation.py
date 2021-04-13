import datetime
from src.tints.db.database import DB


COLLECTION_NAME = "Foundation"
FairFoundation = 'FairFoundation'
LightFoundation = 'LightFoundation'
MediumFoundation = 'MediumFoundation'
TanFoundation = 'TanFoundation'

class Foundation(object):

    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price
        self.created_at = datetime.datetime.utcnow()

    def insert(self,collection_name):
        return DB.insert(collection=collection_name, data=self.json())

    def get_foundation_by_skin_cluster(skin_cluster):
        field = {"brand":1,"name":1,"price":1,"price_sign":1,"currency":1, "image_link":1, "product_link":1, "category": 1, "product_colors":1, "api_featured_image":1}
        if skin_cluster == 0:
            return list(DB.find(collection=LightFoundation, filters={}, field=field))
        elif skin_cluster == 1:
            return list(DB.find(collection=MediumFoundation, filters={}, field=field))
        elif skin_cluster == 2:
            return list(DB.find(collection=FairFoundation, filters={}, field=field))
        else:
            return list(DB.find(collection=TanFoundation, filters={}, field=field))

    def get_foundation_by_skin_type(skin_type_name):
        collection_name = "".join((skin_type_name,COLLECTION_NAME))
        return list(DB.find(collection=collection_name))

    def json(self):
        return {'name':self.name,'product_colors':self.color,'price':self.price, 'created_at':self.created_at}