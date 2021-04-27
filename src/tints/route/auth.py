from flask import request, Blueprint
from flask_cors import CORS
from src.tints.settings import USER_IMAGE_PATH, USER_IMAGE_FILE_TYPE
from src.tints.cv.detector import DetectLandmarks
from src.tints.models.user import User
from flask_jwt_extended import create_access_token,get_jwt_identity, jwt_required
import io
import os
import json
import datetime
import numpy as np
from PIL import Image
from base64 import encodebytes



auth = Blueprint('auth', __name__)
CORS(auth, expose_headers=["x-suggested-filename"],
     resources={r"/*": {"origins": "*"}})

@auth.before_request
def before_request():
    print('Start Auth API request')

@auth.route('/api/check/email/exist', methods=["POST"])
def check_email_exit():
    try:
        email = request.form.get('email')
        user = User(email=email)
        if user.check_is_exist():
            return ("Email already exist", 409)
        else:
            return ("This email avilable to register", 200)
    except:
        return ("Network error", 599)

@auth.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        foundation_list = json.loads(request.form.get('foundation_list'))
        if 'foundation_list' not in request.form:
            return {"detail": "No foundation_list found"}, 400  
        if 'user_image' not in request.files:
            return {"detail": "No file found"}, 400  
        user = User(email=email,password=password)
        if user.check_is_exist():
            return ("User already exist", 400)
        user.hash_password()
        result = user.signup()
        id = str(result)
        User().add_used_foundation(id,foundation_list)
        user_image = request.files['user_image']
        detector = DetectLandmarks()
        user_image = detector.convert_request_files_to_image(user_image)
        detector.save_file(USER_IMAGE_PATH, user_image,"".join((id,USER_IMAGE_FILE_TYPE)))
        return ({'id':id}, 200)
    except Exception as e:
        return {"Error": e}, 400

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    # convert the PIL image to byte array
    pil_img.save(byte_arr, format='JPEG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


@auth.route('/api/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user_info = User().get_user_info_by_email(email)
        user = User()
        user.set_user_info(user_info)
        authorized = user.check_password(password)
        if not authorized:
            return ({'error':'Email or Password invalid'}, 401)
        expires = datetime.timedelta(days=10)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        json = user.login_user_info_json()
        json['token'] = access_token
        user_image_path = os.path.join(USER_IMAGE_PATH,"".join((str(user.id), USER_IMAGE_FILE_TYPE)))
        json['base64_user_image'] = get_response_image(user_image_path)
        return (json, 200)
    except Exception as e:
        return {"Error": e}, 400
    
@auth.route('/api/auth/test/get/user_info/token', methods=['GET'])
@jwt_required()
def get_user_info_from_token_for_test():
    try:
        user_id = get_jwt_identity()
        user_info = User().get_user_info_by_id(user_id)
        user = User()
        user.set_user_info(user_info)
        json = user.login_user_info_json()
        user_image_path = os.path.join(USER_IMAGE_PATH,"".join((str(user.id), USER_IMAGE_FILE_TYPE)))
        json['base64_user_image'] = get_response_image(user_image_path)
        return (json, 200)
    except Exception as e:
        return {"Error": e}, 400

@auth.route('/api/auth/change/password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        user_id = get_jwt_identity()
        user_info = User().get_user_info_by_id(user_id)
        user = User()
        user.set_user_info(user_info)
        authorized = user.check_password(current_password)
        if not authorized:
            return ({'error':'Invalid current password'}, 401)
        user.change_password(new_password)
        return ("Changed password", 200)
    except Exception as e:
        return {"Error": e}, 400

@auth.route('/api/auth/change/user/image', methods=['PUT'])
@jwt_required()
def change_user_image():
    try:
        if 'user_image' not in request.files:
            return {"detail": "No image file found"}, 400
        user_image = request.files['user_image']
        user_id = get_jwt_identity()
        user_info = User().get_user_info_by_id(user_id)
        user = User()
        user.set_user_info(user_info)
        detector = DetectLandmarks()
        new_user_image = detector.convert_request_files_to_image(user_image)
        detector.save_file(USER_IMAGE_PATH, new_user_image,"".join((user_id,USER_IMAGE_FILE_TYPE)))
        return ("Changed user image", 200)
    except Exception as e:
        return {"Error": e}, 400


@auth.route('/api/auth/check/valid/user/image', methods=['POST'])
def check_user_image():
    try:
        if 'user_image' not in request.files:
            return {"detail": "No image file found"}, 400
        user_image = request.files['user_image']
        detector = DetectLandmarks()
        user_image = detector.convert_request_files_to_image(user_image)
        check_is_face = detector.get_landmarks(user_image)
        print("Check type result=",type(check_is_face))
        if isinstance(check_is_face, (np.ndarray, np.generic)):
            return ("Valid User Image", 200)
        else:
            return ("Invalid User Image", 400)
    except Exception as e:
        return {"Error": e}, 400

# This method executes after every API request.
@auth.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response