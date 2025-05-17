from flask import request, jsonify, Blueprint
from extensions import mongo, bcrypt
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from bson import ObjectId

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not last_name or not email or not password or not role:
        return jsonify({"msg": "Faltan campos requeridos"}), 400

    if role not in ['owner', 'walker']:
        return jsonify({"msg": "Rol inválido. Debe ser 'owner' o 'walker'"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"msg": "El email ya está registrado"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = mongo.db.users.insert_one({
        "name": name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password,
        "role": role
    }).inserted_id

    return jsonify({"msg": "Usuario registrado exitosamente", "user_id": str(user_id)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Faltan email o contraseña"}), 400

    user = mongo.db.users.find_one({"email": email})

    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        response_data = {
            "access_token": access_token,
            "role": user.get("role"),
            "name": user.get("name")
        }
        print("Respuesta del login:", response_data)
        return jsonify(response_data), 200
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "Logout exitoso"})
    unset_jwt_cookies(response)
    return response, 200