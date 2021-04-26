from re import S
from src.tints.db.database import DB
from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash


class User(object):

 COLLECTION_NAME = 'Users'
 LIKE_LIPSTICK_FIELD_NAME = 'likedLip'
 LIKE_FOUNDATION_FIELD_NAME = 'likedFoundation'
 LIKE_BLUSH_FIELD_NAME = 'likedBlush'
 USED_FOUNDATION_LIST = 'foundationList'
 COLOR_SELECTED_FIELD = 'colorSelected'

 def __init__(self,id = None,email=None, password=None, foundationList = [], likedLip = [], likedFoundation= [], likedBlush= []):
    self.id = id
    self.email = email
    self.password = password
    self.foundationList = foundationList
    self.likedLip = likedLip
    self.likedFoundation = likedFoundation
    self.likedBlush = likedBlush

 def hash_password(self):
   self.password = generate_password_hash(self.password).decode('utf8')
 
 def check_password(self, password):
   return check_password_hash(self.password, password)

 def check_is_exist(self):
    if list(DB.find(collection=self.COLLECTION_NAME, filters={"email": self.email}, field={})):
        return True
    return False


 def get_user_info_by_id(self,id):
    return  (DB.find(collection=self.COLLECTION_NAME, filters={"_id": ObjectId(id)}, field={"email":1,"password":1,'foundationList':1, 'likedLip':1, 'likedFoundation':1, 'likedBlush':1}))[0]

 def get_user_info_by_email(self,email):
    return  (DB.find(collection=self.COLLECTION_NAME, filters={"email": email}, field={"email":1,"password":1,'foundationList':1, 'likedLip':1, 'likedFoundation':1, 'likedBlush':1}))[0]


 def set_user_info(self,user_info):
     self.id = user_info['_id']
     self.email = user_info['email']
     self.password = user_info['password']
     self.foundationList = user_info['foundationList']
     self.likedLip = user_info['likedLip']
     self.likedFoundation = user_info['likedFoundation']
     self.likedBlush = user_info['likedBlush']

 def signup(self):
    return DB.insert(collection=self.COLLECTION_NAME, data=self.json())
   
 def change_password(self, new_password):
    return DB.update(collection=self.COLLECTION_NAME, filters={"_id" : self.id}, field={ '$set': {'password' : generate_password_hash(new_password).decode('utf8') }})

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

 def get_used_foundation(self):
    return list(DB.find(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(self.id)}, field={self.USED_FOUNDATION_LIST:1}))

 def add_used_foundation(self,id, list_foundation):
    for foundation in list_foundation:
        DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$push': { self.USED_FOUNDATION_LIST : foundation } })

 def delete_used_foundation(self,id, list_foundation):
    for foundation in list_foundation:
        DB.update(collection=self.COLLECTION_NAME, filters={"_id" : ObjectId(id)}, field= { '$pull': { self.USED_FOUNDATION_LIST : foundation } })

 def json(self):
     return {'email':self.email,'password': self.password,'foundationList': [], 'likedLip':[], 'likedFoundation': [], 'likedBlush': []}

 def login_user_info_json(self):
     return {'email':self.email, 'foundationList':  self.foundationList[::-1], 'likedLip':self.likedLip[::-1], 'likedFoundation': self.likedFoundation[::-1], 'likedBlush': self.likedBlush[::-1]}