from flask import Flask
from flask_mongoengine import MongoEngine
from config import DevConfig

# initiating the flask app

app = Flask(__name__)
app.config.from_object(DevConfig)   # setting up the configuration

# the MongoDb database engine start up
db = MongoEngine()
db.init_app(app)



