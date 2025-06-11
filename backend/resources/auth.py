from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, get_jwt_identity
from extensions import mongo, bcrypt
from bson import ObjectId
from utils.email_utils import send_welcome_email, send_reset_email, send_contact_email
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not email or not password or not last_name or not role:
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

    try:
        send_welcome_email(email, name)
    except Exception as e:
        print("Error enviando correo de bienvenida: {}".format(e))

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
        user_role = user.get('role', 'owner')
        access_token = create_access_token(
            identity=email,
            additional_claims={"role": user_role},
            expires_delta=timedelta(hours=1)
        )
        response_data = {
            "access_token": access_token,
            "role": user_role,
            "name": user.get("name"),
            "last_name": user.get("last_name"),
            "email": user.get("email"),
            "id": str(user.get("_id"))
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

@auth_bp.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user_email})

    if user:
        return jsonify({
            "id": str(user["_id"]),
            "name": user.get("name"),
            "last_name": user.get("last_name"),
            "email": user.get("email"),
            "role": user.get("role", "owner")
        }), 200
    return jsonify({"msg": "Usuario no encontrado"}), 404

@auth_bp.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    mongo.db.dogs.delete_many({"owner_id": user["_id"]})
    mongo.db.advertisements.delete_many({"walker_id": user["_id"]})
    mongo.db.requests.delete_many({"$or": [{"owner_id": user["_id"]}, {"walker_id": user["_id"]}]})
    mongo.db.users.delete_one({"_id": user["_id"]})

    return jsonify({"msg": "Usuario y datos eliminados correctamente"}), 200

@auth_bp.route('/update', methods=['PUT', 'POST'])
@jwt_required()
def update_user():
    email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    data = request.get_json()
    update_fields = {}
    if "name" in data:
        update_fields["name"] = data["name"]
    if "last_name" in data:
        update_fields["last_name"] = data["last_name"]
    if "password" in data:
        update_fields["password"] = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    if not update_fields:
        return jsonify({"msg": "No hay campos para actualizar"}), 400

    mongo.db.users.update_one({"_id": user["_id"]}, {"$set": update_fields})

    return jsonify({"msg": "Usuario actualizado correctamente"}), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    email = get_jwt_identity()
    data = request.get_json()
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    user = mongo.db.users.find_one({"email": email})
    if not user or not bcrypt.check_password_hash(user['password'], old_password):
        return jsonify({"msg": "Contraseña actual incorrecta"}), 400
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    mongo.db.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
    return jsonify({"msg": "Contraseña cambiada correctamente"}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"msg": "Si el email existe, se enviará un enlace de recuperación"}), 200

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"reset_token": token, "reset_token_expires": expires}}
    )
    send_reset_email(email, token)
    return jsonify({"msg": "Si el email existe, se enviará un enlace de recuperación"}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({"msg": "Falta la contraseña"}), 400

    user = mongo.db.users.find_one({"reset_token": token})

    if not user:
        return jsonify({"msg": "Token inválido"}), 400

    expires = user.get("reset_token_expires")
    if not expires or datetime.utcnow() > expires:
        return jsonify({"msg": "El enlace ha expirado"}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    mongo.db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {"password": hashed_password},
            "$unset": {"reset_token": "", "reset_token_expires": ""}
        }
    )
    return jsonify({"msg": "Contraseña restablecida correctamente"}), 200


@auth_bp.route('/contact', methods=['POST'])
def contact_form():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({"msg": "Faltan campos requeridos"}), 400

    try:
        send_contact_email(name, email, message)
        return jsonify({"msg": "Mensaje enviado correctamente"}), 200
    except Exception as e:
        print("Error enviando mensaje de contacto: {}".format(e))
        return jsonify({"msg": "Error al enviar el mensaje"}), 500
    
    