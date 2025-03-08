from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from app.utils.db import db
from app.models.role_model import Role
from app.models.user_model import User
from app.routes.auth_routes import auth_bp
from config import Config 

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    with app.app_context():
        db.create_all()  # Ensure tables exist

        # Check and create the Admin role if it does not exist
        admin_role = Role.get_role_by_name('Admin')
        if not admin_role:
            admin_role = Role(name='Admin')
            db.session.add(admin_role)
            db.session.commit()

        # Check if Admin user exists
        admin_user = User.get_by_email('admin@gmail.com')
        if not admin_user:
            admin_user = User(
                firstname='Admin',
                lastname='User',
                email='admin@gmail.com',
                password='123',  
                role_id=admin_role.id
            )
            db.session.add(admin_user)
            db.session.commit()

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
