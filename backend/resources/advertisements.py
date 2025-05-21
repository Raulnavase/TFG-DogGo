from flask import request, jsonify, Blueprint
from extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from utils.decorators import role_required

advertisements_bp = Blueprint('advertisements', __name__, url_prefix='/advertisements')

def get_user_id_from_email(email):
    user = mongo.db.users.find_one({"email": email})
    return user['_id'] if user else None

@advertisements_bp.route('', methods=['POST'])
@jwt_required()
@role_required('walker')
def create_advertisement():
    data = request.get_json()
    biography = data.get('biography')
    maxDogs = data.get('maxDogs')
    locality = data.get('locality')

    if not biography or not maxDogs or not locality:
        return jsonify({"msg": "Faltan campos: biography, maxDogs, locality"}), 400

    current_user_email = get_jwt_identity()
    walker_id = get_user_id_from_email(current_user_email)

    if not walker_id:
        return jsonify({"msg": "Usuario paseador no encontrado"}), 404

    existing_ad = mongo.db.advertisements.find_one({"walker_id": walker_id})
    if existing_ad:
        return jsonify({"msg": "Ya tienes un anuncio. Actualízalo o elimínalo primero."}), 409

    ad_data = {
        "biography": biography,
        "maxDogs": maxDogs,
        "locality": locality,
        "walker_id": walker_id,
        "paused": False
    }
    result = mongo.db.advertisements.insert_one(ad_data)
    ad_data['_id'] = str(result.inserted_id)
    ad_data['walker_id'] = str(ad_data['walker_id'])
    return jsonify({"msg": "Anuncio creado exitosamente", "advertisement": ad_data}), 201

@advertisements_bp.route('', methods=['GET'])
@jwt_required()
@role_required('walker')
def get_my_advertisement():
    current_user_email = get_jwt_identity()
    walker_id = get_user_id_from_email(current_user_email)

    if not walker_id:
        return jsonify({"msg": "Usuario paseador no encontrado"}), 404

    advertisement = mongo.db.advertisements.find_one({"walker_id": walker_id})
    if advertisement:
        advertisement['_id'] = str(advertisement['_id'])
        advertisement['walker_id'] = str(advertisement['walker_id'])
        return jsonify(advertisement), 200
    else:
        return jsonify({"msg": "No tienes un anuncio creado."}), 404

@advertisements_bp.route('/all', methods=['GET'])
@jwt_required()
@role_required('owner')
def get_all_advertisements():
    ads_cursor = mongo.db.advertisements.find({"paused": False})
    ads_list = []
    for ad in ads_cursor:
        ad['_id'] = str(ad['_id'])
        ad['walker_id'] = str(ad['walker_id'])
        ads_list.append(ad)
    return jsonify(ads_list), 200

@advertisements_bp.route('', methods=['PUT'])
@jwt_required()
@role_required('walker')
def update_my_advertisement():
    data = request.get_json()
    current_user_email = get_jwt_identity()
    walker_id = get_user_id_from_email(current_user_email)

    if not walker_id:
        return jsonify({"msg": "Usuario paseador no encontrado"}), 404

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
        return jsonify({"msg": "No hay datos para actualizar"}), 400

    result = mongo.db.advertisements.update_one(
        {"walker_id": walker_id},
        {"$set": update_data}
    )
    if result.matched_count:
        if result.modified_count:
            updated_ad = mongo.db.advertisements.find_one({"walker_id": walker_id})
            updated_ad['_id'] = str(updated_ad['_id'])
            updated_ad['walker_id'] = str(updated_ad['walker_id'])
            return jsonify({"msg": "Anuncio actualizado exitosamente", "advertisement": updated_ad}), 200
        return jsonify({"msg": "No se realizaron cambios en el anuncio"}), 200
    else:
        return jsonify({"msg": "Anuncio no encontrado. Créalo primero."}), 404

@advertisements_bp.route('', methods=['DELETE'])
@jwt_required()
@role_required('walker')
def delete_my_advertisement():
    current_user_email = get_jwt_identity()
    walker_id = get_user_id_from_email(current_user_email)

    if not walker_id:
        return jsonify({"msg": "Usuario paseador no encontrado"}), 404

    result = mongo.db.advertisements.delete_one({"walker_id": walker_id})
    if result.deleted_count:
        return jsonify({"msg": "Anuncio eliminado exitosamente"}), 200
    else:
        return jsonify({"msg": "Anuncio no encontrado."}), 404

@advertisements_bp.route('/pause', methods=['PATCH'])
@jwt_required()
@role_required('walker')
def pause_advertisement():
    current_user_email = get_jwt_identity()
    walker_id = get_user_id_from_email(current_user_email)

    if not walker_id:
        return jsonify({"msg": "Usuario paseador no encontrado"}), 404

    advertisement = mongo.db.advertisements.find_one({"walker_id": walker_id})
    if not advertisement:
        return jsonify({"msg": "Anuncio no encontrado"}), 404

    new_status = not advertisement.get('paused', False)
    result = mongo.db.advertisements.update_one(
        {"walker_id": walker_id},
        {"$set": {"paused": new_status}}
    )
    if result.matched_count:
        advertisement['paused'] = new_status
        advertisement['_id'] = str(advertisement['_id'])
        advertisement['walker_id'] = str(advertisement['walker_id'])
        return jsonify({
            "msg": f"Anuncio {'pausado' if new_status else 'activado'} exitosamente",
            "advertisement": advertisement
        }), 200
    else:
        return jsonify({"msg": "Error al pausar/activar el anuncio"}), 400