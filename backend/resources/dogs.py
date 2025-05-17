from flask import request, jsonify, Blueprint
from extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from utils.decorators import role_required

dogs_bp = Blueprint('dogs', __name__, url_prefix='/dogs')

# Necesitamos obtener el _id del usuario, no solo el email.
# Podríamos guardar el user_id en el token o hacer una consulta extra.
# Para simplificar, haremos una consulta extra.

def get_user_id_from_email(email):
    user = mongo.db.users.find_one({"email": email})
    return user['_id'] if user else None

@dogs_bp.route('', methods=['POST'])
@jwt_required()
@role_required('owner')
def add_dog():
    data = request.get_json()
    dog_name = data.get('name')
    breed = data.get('breed')
    age = data.get('age')

    if not dog_name or not breed or age is None:
        return jsonify({"msg": "Faltan campos: name, breed, age"}), 400

    current_user_email = get_jwt_identity()
    owner_id = get_user_id_from_email(current_user_email)

    if not owner_id:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    dog_data = {
        "name": dog_name,
        "breed": breed,
        "age": age,
        "owner_id": owner_id
    }
    result = mongo.db.dogs.insert_one(dog_data)
    return jsonify({"msg": "Perro añadido exitosamente", "dog_id": str(result.inserted_id)}), 201

@dogs_bp.route('', methods=['GET'])
@jwt_required()
@role_required('owner')
def get_my_dogs():
    current_user_email = get_jwt_identity()
    owner_id = get_user_id_from_email(current_user_email)

    if not owner_id:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    dogs_cursor = mongo.db.dogs.find({"owner_id": owner_id})
    dogs_list = []
    for dog in dogs_cursor:
        dog['_id'] = str(dog['_id'])
        dog['owner_id'] = str(dog['owner_id'])
        dogs_list.append(dog)
    return jsonify(dogs_list), 200

@dogs_bp.route('/<dog_id>', methods=['GET'])
@jwt_required()
@role_required('owner')
def get_dog(dog_id):
    current_user_email = get_jwt_identity()
    owner_id = get_user_id_from_email(current_user_email)

    try:
        obj_dog_id = ObjectId(dog_id)
    except Exception:
        return jsonify({"msg": "ID de perro inválido"}), 400

    dog = mongo.db.dogs.find_one({"_id": obj_dog_id, "owner_id": owner_id})
    if dog:
        dog['_id'] = str(dog['_id'])
        dog['owner_id'] = str(dog['owner_id'])
        return jsonify(dog), 200
    else:
        return jsonify({"msg": "Perro no encontrado o no autorizado"}), 404

@dogs_bp.route('/<dog_id>', methods=['PUT'])
@jwt_required()
@role_required('owner')
def update_dog(dog_id):
    data = request.get_json()
    current_user_email = get_jwt_identity()
    owner_id = get_user_id_from_email(current_user_email)

    try:
        obj_dog_id = ObjectId(dog_id)
    except Exception:
        return jsonify({"msg": "ID de perro inválido"}), 400

    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'breed' in data:
        update_data['breed'] = data['breed']
    if 'age' in data:
        update_data['age'] = data['age']

    if not update_data:
        return jsonify({"msg": "No hay datos para actualizar"}), 400

    result = mongo.db.dogs.update_one(
        {"_id": obj_dog_id, "owner_id": owner_id},
        {"$set": update_data}
    )
    if result.matched_count:
        if result.modified_count:
            return jsonify({"msg": "Perro actualizado exitosamente"}), 200
        return jsonify({"msg": "No se realizaron cambios en el perro"}), 200
    else:
        return jsonify({"msg": "Perro no encontrado o no autorizado"}), 404

@dogs_bp.route('/<dog_id>', methods=['DELETE'])
@jwt_required()
@role_required('owner')
def delete_dog(dog_id):
    current_user_email = get_jwt_identity()
    owner_id = get_user_id_from_email(current_user_email)

    try:
        obj_dog_id = ObjectId(dog_id)
    except Exception:
        return jsonify({"msg": "ID de perro inválido"}), 400

    result = mongo.db.dogs.delete_one({"_id": obj_dog_id, "owner_id": owner_id})
    if result.deleted_count:
        return jsonify({"msg": "Perro eliminado exitosamente"}), 200
    else:
        return jsonify({"msg": "Perro no encontrado o no autorizado"}), 404