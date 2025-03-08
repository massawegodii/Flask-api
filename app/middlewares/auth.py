from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from app.models.user_model import User

def verify_token(role_required=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_email = get_jwt_identity()
                user = User.get_by_email(user_email)

                if not user:
                    return jsonify({"message": "User not found"}), 404

                # Check role if required
                if role_required and user.role.name != role_required:
                    return jsonify({"message": "Unauthorized access"}), 403
                
                return fn(user, *args, **kwargs)

            except Exception as e:
                return jsonify({"message": "Token is invalid or missing", "error": str(e)}), 401
        
        return wrapper
    return decorator
