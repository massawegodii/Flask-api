from app.utils.db import db
from flask_bcrypt import Bcrypt
from datetime import datetime
import re

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def __init__(self, firstname, lastname, email, password, role_id, profile_image=None):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role_id = role_id
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

