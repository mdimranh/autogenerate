from __main__ import app
from pymongo import MongoClient

client = MongoClient(app.config['DB_URL'])
db = client['learn']