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
        
    def json(self):
        return {'name':self.name,'product_colors':self.color,'price':self.price, 'created_at':self.created_at}