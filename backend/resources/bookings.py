from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from utils.decorators import role_required

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

def get_user_id_from_email(email):
    user = mongo.db.users.find_one({"email": email})
    return user['_id'] if user else None

def get_user_name_from_id(user_id):
    user = mongo.db.users.find_one({"_id": user_id})
    return user['name'] if user else "Desconocido"

def get_dog_name_from_id(dog_id):
    dog = mongo.db.dogs.find_one({"_id": dog_id})
    return dog['name'] if dog else "Desconocido"

@bookings_bp.route('/owner', methods=['GET'])
@jwt_required()
@role_required('owner')
def get_owner_bookings():
    current_user_email = get_jwt_identity()
    owner_id = get_user_id_from_email(current_user_email)
    if not owner_id:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    bookings_cursor = mongo.db.bookings.find({"owner_id": owner_id})
    bookings_list = []
    for booking in bookings_cursor:
        booking['_id'] = str(booking['_id'])
        booking['owner_id'] = str(booking['owner_id'])
        booking['walker_id'] = str(booking['walker_id'])
        booking['dog_id'] = str(booking['dog_id'])
        booking['walker_name'] = get_user_name_from_id(booking['walker_id'])
        booking['dog_name'] = get_dog_name_from_id(booking['dog_id'])
        bookings_list.append(booking)
    return jsonify(bookings_list), 200

@bookings_bp.route('/walker', methods=['GET'])
@jwt_required()
@role_required('walker')
def get_walker_bookings():
    current_user_email = get_jwt_identity()
    walker_id = get_user_id_from_email(current_user_email)
    if not walker_id:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    bookings_cursor = mongo.db.bookings.find({"walker_id": walker_id})
    bookings_list = []
    for booking in bookings_cursor:
        booking['_id'] = str(booking['_id'])
        booking['owner_id'] = str(booking['owner_id'])
        booking['walker_id'] = str(booking['walker_id'])
        booking['dog_id'] = str(booking['dog_id'])
        booking['owner_name'] = get_user_name_from_id(booking['owner_id'])
        booking['dog_name'] = get_dog_name_from_id(booking['dog_id'])
        bookings_list.append(booking)
    return jsonify(bookings_list), 200