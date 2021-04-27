from bson import encode
from flask import request, Blueprint
from flask_cors import cross_origin, CORS
from src.tints.models.user import User
from src.tints.models.foundation import Foundation
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.tints.models.user import User
from src.tints.utils.json_encode import JSONEncoder


user = Blueprint('user', __name__)
CORS(user,resources={r"/*": {"origins": "*"}})

@user.before_request
def before_request():
    print('Start User API request')

@user.route('/api/user/liked/lipstick', methods=['POST'])
@jwt_required()
def like_lipstick():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().add_liked_lipstick(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Add like successful", 200)


@user.route('/api/user/liked/foundation', methods=['POST'])
@jwt_required()
def like_foundation():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().add_liked_foundation(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Add like successful", 200)

@user.route('/api/user/liked/blush', methods=['POST'])
@jwt_required()
def like_blush():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().add_liked_blush(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Add like successful", 200)

@user.route('/api/user/delete/liked/lipstick', methods=['POST'])
@jwt_required()
def delete_like_lipstick():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().delete_liked_lipstick(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Delete successful", 200) 

@user.route('/api/user/delete/liked/foundation', methods=['POST'])
@jwt_required()
def delete_like_foundation():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().delete_liked_foundation(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Delete successful", 200) 

@user.route('/api/user/delete/liked/blush', methods=['POST'])
@jwt_required()
def delete_like_blush():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().delete_liked_blush(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Delete successful", 200) 

@user.route('/api/user/get/foundation/info', methods=['GET'])
def get_foundation_info():
    try:
        result = Foundation.get_json_user_register_data()
        return (JSONEncoder().encode(result), 200)
    except:
        return ("Please try again network error", 599)

# @user.route('/api/user/add/used/foundation', methods=['PUT'])
# def add_used_foundation():
#     # try:
#     foundation_list = request.json
#     # print(foundation_list)
#     User().add_used_foundation(foundation_list)
#     return ("Add used foundation list success", 200)
#     # except:
#     #     return ("Please try again network error", 599)

# @user.route('/api/user/delete/used/foundation', methods=['PUT'])
# def delete_used_foundation():
#     try:
#         result = Foundation.get_json_user_register_data()
#         return (JSONEncoder().encode(result), 200)
#     except:
#         return ("Please try again network error", 599)

# This method executes after every API request.
@user.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response