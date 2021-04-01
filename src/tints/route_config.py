import io
import os
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS, cross_origin
from PIL import Image
from base64 import encodebytes
from src.tints.models.lipstick import Lipstick
from src.tints.cv.color_prediction.color_predictor import ColorPredictor
from src.tints.cv.simulation.apply_makeup import ApplyMakeup
from src.tints.db.database import DB
from src.tints.utils.json_encode import JSONEncoder
from src.tints.settings import SIMULATOR_OUTPUT, SIMULATOR_INPUT

# app reference
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# This method executes before any API request


@app.before_request
def before_request():
    print('Start API request')

# Lipstick route path


@app.route('/api/add/lipstick')
def insert_lipstick():
    lipstick = Lipstick('FlukLip', '#EBA38B', 500)
    insert = lipstick.insert()
    return("Success insert id:"+str(insert), 200)


@app.route('/api/lipstick/brand/list')
def get_lipstick_brand():
    brand = Lipstick.distinct_brand()
    return(JSONEncoder().encode(brand), 200)


@app.route('/api/lipstick/list/from/brand')
def get_lipstick_brand_list():
    brand_name = request.args['brand']
    lst = Lipstick.find_lipstick_by_brand(brand_name)
    return(JSONEncoder().encode(lst), 200)


@app.route('/api/color/prediction', methods=['POST'])
@cross_origin()
def prediction():
    # check if the post request has the file part
    if 'ref_face' not in request.files:
        return {"detail": "No file found"}, 400
    ref_face = request.files['ref_face']
    if ref_face.filename == '':
        return {"detail": "Invalid file or filename missing"}, 400
    user_id = request.form.get('user_id')
    color_prediction = ColorPredictor()
    color_prediction.read_image(ref_face, user_id)
    predict_result = color_prediction.get_lipstick_predict()
    return (JSONEncoder().encode(predict_result), 200)


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    # convert the PIL image to byte array
    pil_img.save(byte_arr, format='JPEG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


@app.route('/api/simulator/lip', methods=['POST'])
@cross_origin()
def simulator_lip():
    # check if the post request has the file part
    if 'user_image' not in request.files:
        return {"detail": "No file found"}, 400
    user_image = request.files['user_image']
    # user_image_1 = request.files['user_image_1']
    # user_image_2 = request.files['user_image_2']
    if user_image.filename == '':
        return {"detail": "Invalid file or filename missing"}, 400
    user_id = request.form.get('user_id')
    image_copy_name = 'simulated_image-{}.jpg'.format(str(user_id))
    user_image.save(os.path.join(SIMULATOR_INPUT, image_copy_name))
    rlip = request.form.get('rlip')
    glip = request.form.get('glip')
    blip = request.form.get('blip')
    apply_makeup = ApplyMakeup()

    predict_result_medium = apply_makeup.apply_lipstick(
        image_copy_name, rlip, glip, blip, 51, 51)
    predict_result_fade = apply_makeup.apply_lipstick(
        image_copy_name, rlip, glip, blip, 121, 121)
    predict_result_intense = apply_makeup.apply_lipstick(
        image_copy_name, rlip, glip, blip, 21, 21)

    result = [predict_result_intense,
              predict_result_medium, predict_result_fade]
    encoded_img = []
    for image_path in result:
        encoded_img.append(get_response_image(
            '{}/{}'.format(SIMULATOR_OUTPUT, image_path)))

    return (JSONEncoder().encode(encoded_img), 200)

    # return send_from_directory(
    #     SIMULATOR_OUTPUT,
    #     predict_result_intense,
    #     mimetype='image/jpeg')


# This method executes after every API request.
@app.after_request
def after_request(response):
    return response
