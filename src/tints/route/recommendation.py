from flask import request, Blueprint
from flask_cors import cross_origin, CORS
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.tints.utils.json_encode import JSONEncoder
from src.tints.settings import USER_IMAGE_PATH
from src.tints.cv.recommendation.recommendation import Recommendation


recommendation = Blueprint('recommendation', __name__)

# This method executes before any API request
@recommendation.before_request
def before_request():
    print('Start Recommendation API request')


@recommendation.route('/api/get/recommendation')
@jwt_required()
def get_recommendation():
    try:
        user_id = get_jwt_identity()
        recommendations = Recommendation(str(user_id))
        result = recommendations.get_recommendation()
        print("Start recommendation id:{}, recommend list:{}",user_id, result)
        return (JSONEncoder().encode(result), 200)
    except Exception as e:
        return {"Error": e}, 400


# This method executes after every API request.
@recommendation.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
