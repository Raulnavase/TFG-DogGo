from flask import request, jsonify, Blueprint
from extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from utils.decorators import role_required

advertisements_bp = Blueprint('advertisements', __name__, url_prefix='/advertisements')

def get_user_id_from_email(email): # Reutilizamos la función helper
    user = mongo.db.users.find_one({"email": email})
    return user['_id'] if user else None

@advertisements_bp.route('', methods=['POST'])
@jwt_required()
@role_required('walker')
def create_advertisement():
    data = request.get_json()
    biography = data.get('biography')
    experience = data.get('experience')
    locality = data.get('locality')

    if not biography or not experience or not locality:
        return jsonify({"msg": "Faltan campos: biography, experience, locality"}), 400

    current_user_email = get_jwt_identity()
    walker_id = get_user_id_from_email(current_user_email)

    if not walker_id:
        return jsonify({"msg": "Usuario paseador no encontrado"}), 404

    # Un paseador solo puede tener un anuncio. Verificar si ya existe.
    existing_ad = mongo.db.advertisements.find_one({"walker_id": walker_id})
    if existing_ad:
        return jsonify({"msg": "Ya tienes un anuncio. Actualízalo o elimínalo primero."}), 409

    ad_data = {
        "biography": biography,
        "experience": experience,
        "locality": locality,
        "walker_id": walker_id
    }
    result = mongo.db.advertisements.insert_one(ad_data)
    return jsonify({"msg": "Anuncio creado exitosamente", "advertisement_id": str(result.inserted_id)}), 201

@advertisements_bp.route('', methods=['GET']) # Obtener mi anuncio
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

# Opcional: Ruta pública para ver todos los anuncios (si se desea)
@advertisements_bp.route('/all', methods=['GET'])
def get_all_advertisements():
    ads_cursor = mongo.db.advertisements.find({})
    ads_list = []
    for ad in ads_cursor:
        ad['_id'] = str(ad['_id'])
        ad['walker_id'] = str(ad['walker_id']) # Considerar si exponer el walker_id directamente
        # Podrías querer poblar con algunos datos del paseador (nombre, etc.) en lugar de solo el ID
        ads_list.append(ad)
    return jsonify(ads_list), 200


@advertisements_bp.route('', methods=['PUT']) # Actualizar mi anuncio
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
    if 'experience' in data:
        update_data['experience'] = data['experience']
    if 'locality' in data:
        update_data['locality'] = data['locality']

    if not update_data:
        return jsonify({"msg": "No hay datos para actualizar"}), 400

    result = mongo.db.advertisements.update_one(
        {"walker_id": walker_id},
        {"$set": update_data}
    )
    if result.matched_count:
        if result.modified_count:
            return jsonify({"msg": "Anuncio actualizado exitosamente"}), 200
        return jsonify({"msg": "No se realizaron cambios en el anuncio"}), 200
    else:
        return jsonify({"msg": "Anuncio no encontrado. Créalo primero."}), 404

@advertisements_bp.route('', methods=['DELETE']) # Eliminar mi anuncio
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