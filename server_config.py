import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from src.tints.db.database import DB
from src.tints.route.color_prediction import *
from src.tints.route.recommendation import *
from src.tints.route.simulation import *
from src.tints.route.auth import *
from src.tints.route.user import *

# Load environment config from .env file
load_dotenv()
# App reference
app = Flask(__name__)

CORS(app)
# cors = CORS(app, resources={
#      r"/*":{
#           "origins": "*"
#      }
# })

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.debug = True
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
host = os.environ.get('IP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))


# Register route in application
app.register_blueprint(color_prediction)
app.register_blueprint(recommendation)
app.register_blueprint(simulation)
app.register_blueprint(user)
app.register_blueprint(auth)

# Start connect to MongoDB
DB.init()

if __name__ == "__main__":
    app.run(host=host, port=port)
