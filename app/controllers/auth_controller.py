from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user_model import User
from app.models.role_model import Role
from app.utils.db import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def register():
    data = request.get_json()

    # Validate input data
    if not data.get("firstname") or not data.get("lastname") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    if not User.validate_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    if User.get_by_email(data["email"]):
        return jsonify({"error": "Email is already in use"}), 400

    # Check for Admin role
    admin_role = Role.get_role_by_name('Admin')
    if not admin_role:
        admin_role = Role(name='Admin')
        admin_role.save()

    user = User(
        firstname=data["firstname"],
        lastname=data["lastname"],
        email=data["email"],
        password=data["password"],
        role_id=admin_role.id,
        profile_image=data.get("profile_image")
    )
    user.save()

    return jsonify({"message": "User registered successfully"}), 201

def login():
    data = request.get_json()
    user = User.get_by_email(data["email"])

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify({"access_token": access_token}), 200
