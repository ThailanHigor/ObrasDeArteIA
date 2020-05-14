from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(base_dir, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
API_AZURE = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/fed35364-6f4e-4d46-98db-b13c4389e2d7/classify/iterations/Iteration4/{tipo}'
KEY = '8fb419f53f064296bbaafd37fcba6d63'

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .controllers.home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    return app