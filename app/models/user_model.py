import uuid
from app.utils.db import db
from flask_bcrypt import Bcrypt
from datetime import datetime
import re

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_name = db.Column(db.String(50), nullable=False)

    def __init__(self, firstname, lastname, email, password, role_name, profile_image=None):
        self.id = str(uuid.uuid4())  # Generate UUID for ID
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role_name = role_name.upper()  # Ensure role is always uppercase
        self.profile_image = profile_image

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def save(self):
        if not self.validate_email(self.email):
            raise ValueError("Invalid email format")
        
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def validate_email(email):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email)
