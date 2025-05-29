from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId
from utils.decorators import role_required

advertisements_bp = Blueprint('advertisements', __name__, url_prefix='/advertisements')

@advertisements_bp.route('/create', methods=['POST'])
@jwt_required()
@role_required('walker')
def create_ad():
    data = request.get_json()
    current_user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    existing_ad = mongo.db.advertisements.find_one({"walker_id": user['_id']})
    if existing_ad:
        return jsonify({"msg": "Ya tienes un anuncio creado"}), 400

    ad_data = {
        "walker_id": user['_id'],
        "biography": data.get('biography'),
        "maxDogs": data.get('maxDogs'),
        "locality": data.get('locality'),
        "paused": False
    }
    result = mongo.db.advertisements.insert_one(ad_data)
    return jsonify({"msg": "Anuncio creado", "ad_id": str(result.inserted_id)}), 201

@advertisements_bp.route('/all', methods=['GET'])
@jwt_required()
@role_required('owner')
def get_all_ads():
    locality = request.args.get('locality')
    query = {"paused": False}
    if locality:
        query["locality"] = locality

    ads_cursor = mongo.db.advertisements.find(query)
    ads_list = []
    for ad in ads_cursor:
        ad['_id'] = str(ad['_id'])
        ad['walker_id'] = str(ad['walker_id'])
        walker = mongo.db.users.find_one({"_id": ObjectId(ad['walker_id'])})
        ad['walker_name'] = walker['name'] if walker else 'Desconocido'
        ads_list.append(ad)
    return jsonify(ads_list), 200

@advertisements_bp.route('/walker', methods=['GET'])
@jwt_required()
@role_required('walker')
def get_walker_ad():
    current_user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    ad = mongo.db.advertisements.find_one({"walker_id": user['_id']})
    if not ad:
        return jsonify({"msg": "No tienes un anuncio creado"}), 404

    ad['_id'] = str(ad['_id'])
    ad['walker_id'] = str(ad['walker_id'])
    return jsonify(ad), 200

@advertisements_bp.route('/update', methods=['PUT'])
@jwt_required()
@role_required('walker')
def update_ad():
    data = request.get_json()
    current_user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    ad = mongo.db.advertisements.find_one({"walker_id": user['_id']})
    if not ad:
        return jsonify({"msg": "No tienes un anuncio creado"}), 404

    update_data = {
        "biography": data.get('biography', ad['biography']),
        "maxDogs": data.get('maxDogs', ad['maxDogs']),
        "locality": data.get('locality', ad['locality'])
    }
    mongo.db.advertisements.update_one(
        {"walker_id": user['_id']},
        {"$set": update_data}
    )
    return jsonify({"msg": "Anuncio actualizado"}), 200

@advertisements_bp.route('/toggle-pause', methods=['PATCH'])
@jwt_required()
@role_required('walker')
def toggle_pause_ad():
    current_user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    ad = mongo.db.advertisements.find_one({"walker_id": user['_id']})
    if not ad:
        return jsonify({"msg": "No tienes un anuncio creado"}), 404

    new_status = not ad['paused']
    mongo.db.advertisements.update_one(
        {"walker_id": user['_id']},
        {"$set": {"paused": new_status}}
    )
    return jsonify({"msg": f"Anuncio {'pausado' if new_status else 'activado'}"}), 200

@advertisements_bp.route('/delete', methods=['DELETE'])
@jwt_required()
@role_required('walker')
def delete_ad():
    current_user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    result = mongo.db.advertisements.delete_one({"walker_id": user['_id']})
    if result.deleted_count == 0:
        return jsonify({"msg": "No tienes un anuncio creado"}), 404

    return jsonify({"msg": "Anuncio eliminado"}), 200