from flask import Flask
from models.lipstick import Lipstick
# app reference
app = Flask(__name__)

# This method executes before any API request


@app.before_request
def before_request():
    print('before API request')


@app.route('/api/add/lipstick')
def insert_lipstick():
    lipstick = Lipstick('FlukLip', '#54612', 500)
    insert = lipstick.insert()
    return("Success insert id:"+str(insert), 200)


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
