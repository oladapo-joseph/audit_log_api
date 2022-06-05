from flask import Flask
from flask_mongoengine import MongoEngine
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)   
db = MongoEngine()
db.init_app(app)

      
# the routes

