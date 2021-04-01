from flask import request, Blueprint
from flask_cors import cross_origin
from src.tints.models.lipstick import Lipstick
from src.tints.cv.color_prediction.color_predictor import ColorPredictor
from src.tints.utils.json_encode import JSONEncoder


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


@color_prediction.route('/api/color/prediction', methods=['POST'])
@cross_origin()
def prediction():
    # check if the post request has the file part
    if 'ref_face' not in request.files:
        return {"detail": "No file found"}, 400
    ref_face = request.files['ref_face']
    if ref_face.filename == '':
        return {"detail": "Invalid file or filename missing"}, 400
    user_id = request.form.get('user_id')
    color_prediction = ColorPredictor(ref_face, user_id)
    result = color_prediction.get_all_prediction(request.form.get('blush_hex_color'))
    return (JSONEncoder().encode(result), 200)
    # result = color_prediction.get_blush_predict(request.form.get('blush_hex_color'))
    # return ("JSONEncoder().encode(result)", 200)
    # result = color_prediction.get_foundation_predict()
    # return (JSONEncoder().encode(result), 200)
    # predict_result = color_prediction.get_lipstick_predict()
    # return (JSONEncoder().encode(predict_result), 200)




# This method executes after every API request.
@color_prediction.after_request
def after_request(response):
    return response
