from flask import Flask
from config import Config

app = Flask(__name__)
UPLOAD_FOLDER = './static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)
from app import routes
