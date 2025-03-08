from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///default.db")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token expires in 1 hour
    SQLALCHEMY_TRACK_MODIFICATIONS = False
