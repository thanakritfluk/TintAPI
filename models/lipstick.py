import datetime
from db.database import DB

class Lipstick(object):
    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price
        self.created_at = datetime.datetime.utcnow()

    def insert(self):
        return DB.insert(collection='Lipstick', data=self.json())

    def distinct_brand():
        return DB.distinct(collection='Lipstick',field={},field_distinct="brand")

    def find_lipstick_by_brand(brand):
        return list(DB.find(collection="Lipstick", filters={"brand":brand}, field={"price":1,"name":1,"brand":1, "image_link":1, "product_link":1, "category": 1, "product_colors":1}))

    def json(self):
        return {'name':self.name,'product_colors':self.color,'price':self.price, 'created_at':self.created_at}