from flask import Blueprint
from app.controllers.auth_controller import register, login, update_user_profile
from app.middlewares.auth import verify_token

auth_bp = Blueprint("auth", __name__)
user_bp = Blueprint("user", __name__)


auth_bp.route("/register", methods=["POST"])(register)

auth_bp.route("/login", methods=["POST"])(login)

# Update the user profile
@user_bp.route("/update-profile", methods=["PUT"])
@verify_token()
def update_profile(user):
    return update_user_profile(user)
