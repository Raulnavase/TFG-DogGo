from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import mongo, bcrypt
from bson import ObjectId
from utils.decorators import role_required
from datetime import datetime, timedelta

users_bp = Blueprint('users', __name__, url_prefix='/admin/users')

@users_bp.route('', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_users():
    users_cursor = mongo.db.users.find({})
    users_list = []
    for user in users_cursor:
        user['_id'] = str(user['_id'])
        user.pop('password', None)
        user.pop('reset_token', None)
        user.pop('reset_token_expires', None)
        users_list.append(user)
    return jsonify(users_list), 200

@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_user_details(user_id):
    try:
        obj_user_id = ObjectId(user_id)
    except Exception:
        return jsonify({"msg": "ID de usuario inválido"}), 400

    user = mongo.db.users.find_one({"_id": obj_user_id})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    user['_id'] = str(user['_id'])
    user.pop('password', None)
    user.pop('reset_token', None)
    user.pop('reset_token_expires', None)

    advertisements = []
    if user.get('role') == 'walker':
        ads_cursor = mongo.db.advertisements.find({"walker_id": obj_user_id})
        for ad in ads_cursor:
            ad['_id'] = str(ad['_id'])
            ad['walker_id'] = str(ad['walker_id'])
            advertisements.append(ad)

    dogs = []
    if user.get('role') == 'owner':
        dogs_cursor = mongo.db.dogs.find({"owner_id": obj_user_id})
        for dog in dogs_cursor:
            dog['_id'] = str(dog['_id'])
            dog['owner_id'] = str(dog['owner_id'])
            dogs.append(dog)

    requests_list = []
    reqs_cursor = mongo.db.requests.find({"$or": [{"owner_id": obj_user_id}, {"walker_id": obj_user_id}]})
    for req in reqs_cursor:
        req['_id'] = str(req['_id'])
        req_owner_id = req['owner_id']
        req_walker_id = req['walker_id']
        req_ad_id = req['ad_id']
        req_dogs_ids = req['dogs']

        owner_info = mongo.db.users.find_one({"_id": req_owner_id}, {"name": 1, "last_name": 1, "email": 1})
        req['owner_info'] = {
            "id": str(owner_info['_id']),
            "name": owner_info['name'],
            "last_name": owner_info['last_name'],
            "email": owner_info['email']
        } if owner_info else {"id": None, "name": "N/A", "last_name": "", "email": "N/A"}

        walker_info = mongo.db.users.find_one({"_id": req_walker_id}, {"name": 1, "last_name": 1, "email": 1})
        req['walker_info'] = {
            "id": str(walker_info['_id']),
            "name": walker_info['name'],
            "last_name": walker_info['last_name'],
            "email": walker_info['email']
        } if walker_info else {"id": None, "name": "N/A", "last_name": "", "email": "N/A"}

        dogs_info = []
        if req_dogs_ids:
            dogs_cursor = mongo.db.dogs.find({"_id": {"$in": req_dogs_ids}})
            for dog in dogs_cursor:
                dogs_info.append({
                    "id": str(dog['_id']),
                    "name": dog['name'],
                    "breed": dog['breed'],
                    "age": dog['age']
                })
        req['dogs_info'] = dogs_info

        req['owner_id'] = str(req_owner_id)
        req['walker_id'] = str(req_walker_id)
        req['ad_id'] = str(req_ad_id)
        req['dogs'] = [str(d) for d in req_dogs_ids]

        requests_list.append(req)

    user_details = {
        "user": user,
        "advertisements": advertisements,
        "dogs": dogs,
        "requests": requests_list
    }
    return jsonify(user_details), 200

@users_bp.route('', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_user():
    data = request.get_json()
    name = data.get('name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not email or not password or not last_name or not role:
        return jsonify({"msg": "Faltan campos requeridos"}), 400

    if role not in ['owner', 'walker', 'admin']:
        return jsonify({"msg": "Rol inválido. Debe ser 'owner', 'walker' o 'admin'"}), 400

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

    return jsonify({"msg": "Usuario creado exitosamente", "user_id": str(user_id)}), 201

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user_by_admin(user_id):
    try:
        obj_user_id = ObjectId(user_id)
    except Exception:
        return jsonify({"msg": "ID de usuario inválido"}), 400

    user = mongo.db.users.find_one({"_id": obj_user_id})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    data = request.get_json()
    update_fields = {}

    if "name" in data:
        update_fields["name"] = data["name"]
    if "last_name" in data:
        update_fields["last_name"] = data["last_name"]
    if "email" in data and data["email"] != user["email"]:
        if mongo.db.users.find_one({"email": data["email"]}):
            return jsonify({"msg": "El nuevo email ya está en uso"}), 409
        update_fields["email"] = data["email"]
    if "password" in data and data["password"]:
        update_fields["password"] = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    if "role" in data and data["role"] in ['owner', 'walker', 'admin']:
        update_fields["role"] = data["role"]

    if not update_fields:
        return jsonify({"msg": "No hay campos para actualizar"}), 400

    mongo.db.users.update_one({"_id": obj_user_id}, {"$set": update_fields})

    return jsonify({"msg": "Usuario actualizado correctamente"}), 200


@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user_by_admin(user_id):
    try:
        obj_user_id = ObjectId(user_id)
    except Exception:
        return jsonify({"msg": "ID de usuario inválido"}), 400

    user_to_delete = mongo.db.users.find_one({"_id": obj_user_id})
    if not user_to_delete:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    current_admin_email = get_jwt_identity()
    current_admin = mongo.db.users.find_one({"email": current_admin_email})
    if current_admin and current_admin['_id'] == obj_user_id:
        return jsonify({"msg": "Un administrador no puede eliminarse a sí mismo"}), 403

    mongo.db.dogs.delete_many({"owner_id": obj_user_id})
    mongo.db.advertisements.delete_many({"walker_id": obj_user_id})
    mongo.db.requests.delete_many({"$or": [{"owner_id": obj_user_id}, {"walker_id": obj_user_id}]})

    mongo.db.users.delete_one({"_id": obj_user_id})

    return jsonify({"msg": "Usuario y datos asociados eliminados correctamente"}), 200


@users_bp.route('/advertisements/<ad_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_advertisement_by_admin(ad_id):
    try:
        obj_ad_id = ObjectId(ad_id)
    except Exception:
        return jsonify({"msg": "ID de anuncio inválido"}), 400

    result = mongo.db.advertisements.delete_one({"_id": obj_ad_id})
    if result.deleted_count == 0:
        return jsonify({"msg": "Anuncio no encontrado"}), 404
    return jsonify({"msg": "Anuncio eliminado por administrador"}), 200

@users_bp.route('/advertisements/<ad_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_advertisement_by_admin(ad_id):
    try:
        obj_ad_id = ObjectId(ad_id)
    except Exception:
        return jsonify({"msg": "ID de anuncio inválido"}), 400

    data = request.get_json()
    update_data = {}
    if 'biography' in data:
        update_data['biography'] = data['biography']
    if 'maxDogs' in data:
        update_data['maxDogs'] = data['maxDogs']
    if 'locality' in data:
        update_data['locality'] = data['locality']
    if 'paused' in data:
        update_data['paused'] = data['paused']

    if not update_data:
        return jsonify({"msg": "No hay campos para actualizar"}), 400

    result = mongo.db.advertisements.update_one({"_id": obj_ad_id}, {"$set": update_data})
    if result.matched_count == 0:
        return jsonify({"msg": "Anuncio no encontrado"}), 404
    return jsonify({"msg": "Anuncio actualizado por administrador"}), 200

@users_bp.route('/dogs/<dog_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_dog_by_admin(dog_id):
    try:
        obj_dog_id = ObjectId(dog_id)
    except Exception:
        return jsonify({"msg": "ID de perro inválido"}), 400

    result = mongo.db.dogs.delete_one({"_id": obj_dog_id})
    if result.deleted_count == 0:
        return jsonify({"msg": "Perro no encontrado"}), 404
    return jsonify({"msg": "Perro eliminado por administrador"}), 200

@users_bp.route('/dogs/<dog_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_dog_by_admin(dog_id):
    try:
        obj_dog_id = ObjectId(dog_id)
    except Exception:
        return jsonify({"msg": "ID de perro inválido"}), 400

    data = request.get_json()
    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'breed' in data:
        update_data['breed'] = data['breed']
    if 'age' in data:
        update_data['age'] = data['age']
    if 'owner_id' in data:
        try:
            update_data['owner_id'] = ObjectId(data['owner_id'])
        except Exception:
            return jsonify({"msg": "ID de owner inválido"}), 400

    if not update_data:
        return jsonify({"msg": "No hay campos para actualizar"}), 400

    result = mongo.db.dogs.update_one({"_id": obj_dog_id}, {"$set": update_data})
    if result.matched_count == 0:
        return jsonify({"msg": "Perro no encontrado"}), 404
    return jsonify({"msg": "Perro actualizado por administrador"}), 200

@users_bp.route('/requests/<request_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_request_by_admin(request_id):
    try:
        obj_request_id = ObjectId(request_id)
    except Exception:
        return jsonify({"msg": "ID de solicitud inválido"}), 400

    result = mongo.db.requests.delete_one({"_id": obj_request_id})
    if result.deleted_count == 0:
        return jsonify({"msg": "Solicitud no encontrada"}), 404
    return jsonify({"msg": "Solicitud eliminada por administrador"}), 200

@users_bp.route('/requests/<request_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_request_by_admin(request_id):
    try:
        obj_request_id = ObjectId(request_id)
    except Exception:
        return jsonify({"msg": "ID de solicitud inválido"}), 400

    data = request.get_json()
    update_data = {}

    if 'owner_id' in data:
        try:
            update_data['owner_id'] = ObjectId(data['owner_id'])
        except Exception:
            return jsonify({"msg": "ID de owner inválido"}), 400
    if 'walker_id' in data:
        try:
            update_data['walker_id'] = ObjectId(data['walker_id'])
        except Exception:
            return jsonify({"msg": "ID de walker inválido"}), 400
    if 'ad_id' in data:
        try:
            update_data['ad_id'] = ObjectId(data['ad_id'])
        except Exception:
            return jsonify({"msg": "ID de anuncio inválido"}), 400
    if 'date' in data:
        update_data['date'] = data['date']
    if 'dogs' in data and isinstance(data['dogs'], list):
        try:
            update_data['dogs'] = [ObjectId(d) for d in data['dogs']]
        except Exception:
            return jsonify({"msg": "ID de perro(s) inválido(s) en la lista de perros"}), 400
    if 'status' in data and data['status'] in ['pendiente', 'aceptada', 'rechazada', 'cancelada_por_owner', 'cancelada_por_walker']:
        update_data['status'] = data['status']

    if not update_data:
        return jsonify({"msg": "No hay campos para actualizar"}), 400

    result = mongo.db.requests.update_one({"_id": obj_request_id}, {"$set": update_data})
    if result.matched_count == 0:
        return jsonify({"msg": "Solicitud no encontrada"}), 404
    return jsonify({"msg": "Solicitud actualizada por administrador"}), 200