from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from extensions import mongo

def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_email = get_jwt_identity()
            user = mongo.db.users.find_one({"email": user_email})
            if user and user.get("role") == role_name:
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": f"Acceso denegado: Se requiere rol '{role_name}'"}), 403
        return wrapper
    return decorator