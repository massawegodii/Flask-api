from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user_model import User
from app.utils.db import db

def register():
    data = request.get_json()
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    if User.get_by_username(data["username"]):
        return jsonify({"error": "User already exists"}), 400

    user = User(username=data["username"], password=data["password"])
    user.save()

    return jsonify({"message": "User registered successfully"}), 201

def login():
    data = request.get_json()
    user = User.get_by_username(data["username"])

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify({"access_token": access_token}), 200
