import io
import os
from flask import Flask, request, send_from_directory, jsonify, Blueprint
from flask_cors import cross_origin, CORS
from PIL import Image
from base64 import encodebytes
from src.tints.utils.json_encode import JSONEncoder
from src.tints.cv.simulation.apply_makeup import ApplyMakeup
from src.tints.settings import SIMULATOR_INPUT, SIMULATOR_OUTPUT


simulation = Blueprint('simulation', __name__)
CORS(simulation)
# This method executes before any API request


@simulation.before_request
def before_request():
    print('Start Simulation API request')


@simulation.route('/api/test/simulation')
def test_simulation():
    return("Success get simulation api call", 200)


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    # convert the PIL image to byte array
    pil_img.save(byte_arr, format='JPEG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


@simulation.route('/api/simulator/lip', methods=['POST'])
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
    r_value = request.form.get('r_value')
    g_value = request.form.get('g_value')
    b_value = request.form.get('b_value')
    apply_makeup = ApplyMakeup()

    predict_result_medium = apply_makeup.apply_lipstick(
        image_copy_name, r_value, g_value, b_value, 51, 51)
    predict_result_fade = apply_makeup.apply_lipstick(
        image_copy_name, r_value, g_value, b_value, 121, 121)
    predict_result_intense = apply_makeup.apply_lipstick(
        image_copy_name, r_value, g_value, b_value, 21, 21)

    result = [predict_result_intense,
              predict_result_medium, predict_result_fade]
    encoded_img = []
    for image_path in result:
        encoded_img.append(get_response_image(
            '{}/{}'.format(SIMULATOR_OUTPUT, image_path)))

    return (JSONEncoder().encode(encoded_img), 200)


@simulation.route('/api/simulator/blush', methods=['POST'])
def simulator_value():
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
    r_value = request.form.get('r_value')
    g_value = request.form.get('g_value')
    b_value = request.form.get('b_value')
    apply_makeup = ApplyMakeup()

    predict_result_fade = apply_makeup.apply_blush(
        image_copy_name, r_value, g_value, b_value, 121, 121, 0.1)
    predict_result_medium = apply_makeup.apply_blush(
        image_copy_name, r_value, g_value, b_value, 81, 81, 0.15)
    predict_result_intense = apply_makeup.apply_blush(
        image_copy_name, r_value, g_value, b_value, 41, 41, 0.15)

    result = [predict_result_intense,
              predict_result_medium, predict_result_fade]
    encoded_img = []
    for image_path in result:
        encoded_img.append(get_response_image(
            '{}/{}'.format(SIMULATOR_OUTPUT, image_path)))

    return (JSONEncoder().encode(encoded_img), 200)
    # return send_from_directory(
    #     SIMULATOR_OUTPUT,
    #     predict_result_medium,
    #     mimetype='image/jpeg')


@simulation.route('/api/simulator/foundation', methods=['POST'])
def foundation_value():
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
    r_value = request.form.get('r_value')
    g_value = request.form.get('g_value')
    b_value = request.form.get('b_value')
    apply_makeup = ApplyMakeup()

    predict_result_fade = apply_makeup.apply_foundation(
        image_copy_name, r_value, g_value, b_value, 121, 121, 0.3)
    predict_result_medium = apply_makeup.apply_foundation(
        image_copy_name, r_value, g_value, b_value, 77, 77, 0.5)
    predict_result_intense = apply_makeup.apply_foundation(
        image_copy_name, r_value, g_value, b_value, 75, 75, 1.1)

    result = [predict_result_intense,
              predict_result_medium, predict_result_fade]
    encoded_img = []
    for image_path in result:
        encoded_img.append(get_response_image(
            '{}/{}'.format(SIMULATOR_OUTPUT, image_path)))

    return (JSONEncoder().encode(encoded_img), 200)
    return send_from_directory(
        SIMULATOR_OUTPUT,
        predict_result_medium,
        mimetype='image/jpeg')

# This method executes after every API request.


@simulation.after_request
def after_request(response):
    return response
