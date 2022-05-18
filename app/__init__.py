from flask import Flask
from config import Config
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
UPLOAD_FOLDER = './static/img'
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes
from .models import empresa, cargo, funcionario, funcionario_ponto
from .views import empresa

db.create_all(app=app)