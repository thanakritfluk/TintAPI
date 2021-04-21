from re import S
from src.tints.db.database import DB
from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash


class User(object):

 COLLECTION_NAME = 'Users'
 LIKE_LIPSTICK_FIELD_NAME = 'likedLip'
 LIKE_FOUNDATION_FIELD_NAME = 'likedFoundation'
 LIKE_BLUSH_FIELD_NAME = 'likedBlush'

 def __init__(self,id = None,email=None, password=None):
    self.id = id
    self.email = email
    self.password = password

 def hash_password(self):
   self.password = generate_password_hash(self.password).decode('utf8')
 
 def check_password(self, password):
   return check_password_hash(self.password, password)

 def check_is_exist(self):
    if list(DB.find(collection=self.COLLECTION_NAME, filters={"email": self.email}, field={})):
        return True
    return False

 def set_user_info_by_email(self,email):
     user_info = (DB.find(collection=self.COLLECTION_NAME, filters={"email":email}, field={"email":1,"password":1}))[0]
     return user_info

 def signup(self):
    return DB.insert(collection=self.COLLECTION_NAME, data=self.json())

 def add_liked_lipstick(self, id, json):
    return DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$push': { self.LIKE_LIPSTICK_FIELD_NAME : json } })

 def add_liked_foundation(self, id, json):
    return DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$push': { self.LIKE_FOUNDATION_FIELD_NAME : json } })

 def add_liked_blush(self, id, json):
    return DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$push': { self.LIKE_BLUSH_FIELD_NAME : json } })

 def delete_liked_lipstick(self, id, json):
    return DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$pull': { self.LIKE_LIPSTICK_FIELD_NAME : json } })

 def delete_liked_foundation(self, id, json):
    return DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$pull': { self.LIKE_FOUNDATION_FIELD_NAME : json } })

 def delete_liked_blush(self, id, json):
    return DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$pull': { self.LIKE_BLUSH_FIELD_NAME : json } })

 def json(self):
     return {'email':self.email,'password': self.password,'foundationList': [], 'likedLip':[], 'likedFoundation': [], 'likedBlush': []}