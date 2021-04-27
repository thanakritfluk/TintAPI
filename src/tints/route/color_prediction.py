from flask import request, Blueprint, send_file
from flask_cors import cross_origin
from src.tints.models.lipstick import Lipstick
from src.tints.cv.color_prediction.color_predictor import ColorPredictor
from src.tints.cv.detector import DetectLandmarks
from src.tints.settings import COLOR_PREDICTION_INPUT, SAVE_FILE_TYPE
from src.tints.utils.json_encode import JSONEncoder
from os.path import join as pjoin
import time
import asyncio
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from src.tints.utils.async_function import async_action


color_prediction = Blueprint('color_prediction', __name__)

# This method executes before any API request


@color_prediction.before_request
def before_request():
    print('Start Color Prediction API request')


@color_prediction.route('/api/add/lipstick')
def insert_lipstick():
    lipstick = Lipstick('FlukLip', '#EBA38B', 500)
    insert = lipstick.insert()
    return("Success insert id:"+str(insert), 200)


@color_prediction.route('/api/lipstick/brand/list')
def get_lipstick_brand():
    brand = Lipstick.distinct_brand()
    return(JSONEncoder().encode(brand), 200)


@color_prediction.route('/api/lipstick/list/from/brand')
def get_lipstick_brand_list():
    brand_name = request.args['brand']
    lst = Lipstick.find_lipstick_by_brand(brand_name)
    return(JSONEncoder().encode(lst), 200)

# Method 1 required cheek color at first


@color_prediction.route('/api/v1/get/prediction/color', methods=['POST'])
@jwt_required()
@cross_origin()
def prediction():
    current_user = get_jwt_identity()
    # check if the post request has the file part
    if 'ref_face' not in request.files:
        return {"detail": "No file found"}, 400
    ref_face = request.files['ref_face']
    if ref_face.filename == '':
        return {"detail": "Invalid file or filename missing"}, 400
    user_id = current_user
    color_prediction = ColorPredictor(user_id)
    color_prediction.read_image_from_request_file(ref_face)
    result = color_prediction.get_all_prediction(
        request.form.get('blush_hex_color'))
    return (JSONEncoder().encode(result), 200)
    # result = color_prediction.get_blush_predict(request.form.get('blush_hex_color'))
    # return ("JSONEncoder().encode(result)", 200)
    # result = color_prediction.get_foundation_predict()
    # return (JSONEncoder().encode(result), 200)
    # predict_result = color_prediction.get_lipstick_predict()
    # return (JSONEncoder().encode(predict_result), 200)


@color_prediction.route('/api/v2/get/cheek/image', methods=['POST'])
@jwt_required()
@cross_origin()
def get_cheek_image():
    try:
        current_user = get_jwt_identity()
        print("Current user =", current_user)
        if 'ref_face' not in request.files:
            return {"detail": "No file found"}, 400
        ref_face = request.files['ref_face']
        user_id = current_user
        detector = DetectLandmarks()
        ref_face_img = detector.convert_request_files_to_image(ref_face)
        cheek_np = detector.get_cheek_np(ref_face_img)
        base_image_name = "".join((user_id, "_", time.strftime('%H-%M-%S')))
        save_image_name = "".join((base_image_name, SAVE_FILE_TYPE))
        save_image_original_name = "".join((user_id, SAVE_FILE_TYPE))
        detector.save_file(COLOR_PREDICTION_INPUT, ref_face_img,
                        save_image_original_name)
        detector.create_box(ref_face_img, COLOR_PREDICTION_INPUT,
                            base_image_name, cheek_np)
        image_path = pjoin(COLOR_PREDICTION_INPUT, save_image_name)
        response = send_file(image_path, mimetype='image/jpeg',
                            as_attachment=True)
        response.headers["x-suggested-filename"] = save_image_name

        return response
    except Exception as e:
        return {"Error": e}, 400

# Method 2 required cheeck color after user pickle from cheek image


@color_prediction.route('/api/v2/get/prediction/color', methods=['POST'])
@jwt_required()
@cross_origin()
def get_color_prediction():
    try:
        current_user = get_jwt_identity()
        user_id = current_user
        filename = "".join((user_id, SAVE_FILE_TYPE))
        color_prediction = ColorPredictor(user_id, "COLOR_PREDICTION_FILE_READ")
        color_prediction.read_image_from_storage(filename)
        # await asyncio.sleep(4)
        print("Start get prediction color id:{}, filename:{}, blush color:{}".format(user_id, filename,request.form.get('blush_hex_color')))
        result = color_prediction.get_all_prediction(
            request.form.get('blush_hex_color'))
        return (JSONEncoder().encode(result), 200)
    except Exception as e:
        return {"Error": e}, 400


# This method executes after every API request.
@color_prediction.after_request
def after_request(response):
    return response
