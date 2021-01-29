import os
from src.tints.route_config import *
from src.tints.db.database import DB
from dotenv import load_dotenv 

load_dotenv()
app.debug = True
host = os.environ.get('IP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))
DB.init()

if __name__ == "__main__":
    app.run(host=host, port=port)