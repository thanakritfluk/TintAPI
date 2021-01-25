from flask import Flask, request
# from models.lipstick import Lipstick
from src.tints.cv.lipstick_detection import predict_lipstick_color
from src.tints.db.database import DB
from src.tints.utils.json_encode import JSONEncoder
# app reference
app = Flask(__name__)

# This method executes before any API request
@app.before_request
def before_request():
    print('before API request')


# @app.route('/api/add/lipstick')
# def insert_lipstick():
#     lipstick = Lipstick('FlukLip', '#EBA38B', 500)
#     insert = lipstick.insert()
#     return("Success insert id:"+str(insert), 200)

# @app.route('/api/lipstick/brand')
# def get_lipstick_brand():
#     brand = Lipstick.distinct_brand()
#     print("All brand =",brand)
#     return("Success",200)

# @app.route('/api/lipstick/brand/list')
# def get_lipstick_brand_list():
#     brand_name = request.args['brand']
#     lst = Lipstick.find_lipstick_by_brand(brand_name)
#     for i in  lst:
#         print(i)
#         print()
#     return("Return list of lipstick brand",200)

@app.route('/api/prediction/lipstick', methods=['POST'])
def predict_lipstick():
    # check if the post request has the file part
    if 'ref_face' not in request.files:
        return {"detail": "No file found"}, 400
    ref_face = request.files['ref_face']
    if ref_face.filename == '':
        return {"detail": "Invalid file or filename missing"}, 400
    result = predict_lipstick_color(ref_face)
    return (JSONEncoder().encode(result), 200)

# # This is POST method which stores foundation.
# @app.route('/api/foundation', methods=['POST'])
# def store_foundation_data():
#     return "foundation list[POST]"

# This method executes after every API request.
@app.after_request
def after_request(response):
    return response
