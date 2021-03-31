from flask import request, Blueprint
from flask_cors import cross_origin
from src.tints.utils.json_encode import JSONEncoder


simulation_route = Blueprint('simulation_route', __name__)

# This method executes before any API request
@simulation_route.before_request
def before_request():
    print('Start Simulation API request')


@simulation_route.route('/api/test/simulation')
def test_simulation():
    return("Success get simulation api call", 200)


# This method executes after every API request.
@simulation_route.after_request
def after_request(response):
    return response
