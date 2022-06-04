import os
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES

UPLOAD_FOLDER = os.path.join(Path(__file__).parent.absolute(), 'static')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_IMAGES_DEST'] = os.path.join(UPLOAD_FOLDER, 'images')

images = UploadSet('images', IMAGES)

configure_uploads(app, (images,))

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import *
from app import views
from app import auth
