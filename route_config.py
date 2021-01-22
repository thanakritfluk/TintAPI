from flask import Flask, request
from "/models/lipstick.py" import Lipstick
from detection.detector import face_detect
# app reference
app = Flask(__name__)

# This method executes before any API request


@app.before_request
def before_request():
    print('before API request')


@app.route('/api/add/lipstick')
def insert_lipstick():
    lipstick = Lipstick('FlukLip', '#EBA38B', 500)
    insert = lipstick.insert()
    return("Success insert id:"+str(insert), 200)


@app.route('/api/prediction/lipstick', methods=['POST'])
def predict_lipstick():
    # check if the post request has the file part
    if 'ref_face' not in request.files:
        return {"detail": "No file found"}, 400
    ref_face = request.files['ref_face']
    if ref_face.filename == '':
        return {"detail": "Invalid file or filename missing"}, 400
    file_type = (ref_face.content_type).split('/')[1]
    file_path = "./image/input/source." + file_type
    ref_face.save(file_path)
    face_detect(file_path,file_type)
    return "Success"


# This method returns lipstick
@app.route('/api/lipstick')
def get_lipstick_list():
    return "Lipstick list[GET]"

# This is POST method which stores foundation.


@app.route('/api/foundation', methods=['POST'])
def store_foundation_data():
    return "foundation list[POST]"

# This method executes after every API request.


@app.after_request
def after_request(response):
    return response
