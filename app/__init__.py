from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import uuid

from app.utils.db import db
from app.models.role_model import Role
from app.models.user_model import User
from app.routes.auth_routes import auth_bp
from app.routes.auth_routes import user_bp
from config import Config 

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    with app.app_context():
        db.create_all()  

        # Ensure all roles exist
        Role.ensure_roles_exist()

        # Check if Admin user exists
        admin_user = User.get_by_email('admin@gmail.com')
        if not admin_user:
            admin_user = User(
                firstname='Godfrey',
                lastname='Matias',
                email='admin@gmail.com',
                password='123',  
                role_name='ADMIN'
            )
            db.session.add(admin_user)
            db.session.commit()

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")

    return app
