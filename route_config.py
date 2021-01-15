from flask import Flask
# app reference
app = Flask(__name__)

# This method executes before any API request
@app.before_request
def before_request():
    print('before API request')

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