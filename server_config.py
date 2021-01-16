import os
from route_config import *
from db.database import DB

app.debug = True
host = os.environ.get('IP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))
DB.init()
app.run(host=host, port=port)