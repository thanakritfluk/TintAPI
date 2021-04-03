import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src.tints.db.database import DB
from src.tints.route.color_prediction import *
from src.tints.route.recommendation import *
from src.tints.route.simulation import *

# Load environment config from .env file
load_dotenv()
# App reference
app = Flask(__name__)
app.debug = True
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, expose_headers=["x-suggested-filename"],
     resources={r"/*": {"origins": "*"}})
host = os.environ.get('IP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))

# Register route in application
app.register_blueprint(color_prediction)
app.register_blueprint(recommendation)
app.register_blueprint(simulation)

# Start connect to MongoDB
DB.init()

if __name__ == "__main__":
    app.run(host=host, port=port)
