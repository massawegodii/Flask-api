from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from app.utils.db import db
from app.routes.auth_routes import auth_bp
from config import Config 

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations from Config class

    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
