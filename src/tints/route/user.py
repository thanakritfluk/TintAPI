from flask import request, Blueprint
from flask_cors import cross_origin
from src.tints.models.user import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.tints.models.user import User


user = Blueprint('user', __name__)


@user.before_request
def before_request():
    print('Start User API request')

@user.route('/api/user/liked/lipstick', methods=['POST'])
@jwt_required()
@cross_origin()
def like_lipstick():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().add_liked_lipstick(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Add like successful", 200)


@user.route('/api/user/liked/foundation', methods=['POST'])
@jwt_required()
@cross_origin()
def like_foundation():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().add_liked_foundation(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Add like successful", 200)

@user.route('/api/user/liked/blush', methods=['POST'])
@jwt_required()
@cross_origin()
def like_blush():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().add_liked_blush(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Add like successful", 200)

@user.route('/api/user/delete/liked/lipstick', methods=['POST'])
@jwt_required()
@cross_origin()
def delete_like_lipstick():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().delete_liked_lipstick(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Delete successful", 200) 

@user.route('/api/user/delete/liked/foundation', methods=['POST'])
@jwt_required()
@cross_origin()
def delete_like_foundation():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().delete_liked_foundation(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Delete successful", 200) 

@user.route('/api/user/delete/liked/blush', methods=['POST'])
@jwt_required()
@cross_origin()
def delete_like_blush():
    like_json_object = request.json
    user_id = get_jwt_identity()
    result = User().delete_liked_blush(user_id, like_json_object)
    if not result['updatedExisting']:
        return ("Error Please Try Again", 400)
    return ("Delete successful", 200) 

# This method executes after every API request.
@user.after_request
def after_request(response):
    return response