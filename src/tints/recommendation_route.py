from flask import request, Blueprint
from flask_cors import cross_origin
from src.tints.utils.json_encode import JSONEncoder


recommendation_route = Blueprint('recommendation_route', __name__)

# This method executes before any API request
@recommendation_route.before_request
def before_request():
    print('Start Recommendation API request')


@recommendation_route.route('/api/test/recommendation')
def test_simulation():
    return("Success get recommendation api call", 200)


# This method executes after every API request.
@recommendation_route.after_request
def after_request(response):
    return response
