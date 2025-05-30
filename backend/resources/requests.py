from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId
from utils.decorators import role_required
from datetime import datetime

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

@requests_bp.route('', methods=['POST'])
@jwt_required()
@role_required('owner')
def create_request():
    data = request.get_json()
    current_email = get_jwt_identity()
    owner = get_user_by_email(current_email)
    if not owner:
        return jsonify({"msg": "Owner no encontrado"}), 404

    walker_id = data.get('walker_id')
    ad_id = data.get('ad_id')
    date = data.get('date')
    dogs = data.get('dogs')

    if not walker_id or not ad_id or not date or not dogs:
        return jsonify({"msg": "Faltan campos obligatorios"}), 400

    existing = mongo.db.requests.find_one({
        "owner_id": owner['_id'],
        "walker_id": ObjectId(walker_id),
        "ad_id": ObjectId(ad_id),
        "date": date,
        "status": {"$in": ["pendiente", "aceptada"]}
    })
    if existing:
        return jsonify({"msg": "Ya tienes una solicitud pendiente o aceptada para este anuncio y fecha"}), 400

    req = {
        "owner_id": owner['_id'],
        "walker_id": ObjectId(walker_id),
        "ad_id": ObjectId(ad_id),
        "date": date,
        "dogs": [ObjectId(d) for d in dogs],
        "status": "pendiente",
        "created_at": datetime.utcnow()
    }
    result = mongo.db.requests.insert_one(req)
    return jsonify({"msg": "Solicitud creada", "request_id": str(result.inserted_id)}), 201

@requests_bp.route('/owner', methods=['GET'])
@jwt_required()
@role_required('owner')
def get_owner_requests():
    current_email = get_jwt_identity()
    owner = get_user_by_email(current_email)
    if not owner:
        return jsonify({"msg": "Owner no encontrado"}), 404

    reqs = mongo.db.requests.find({"owner_id": owner['_id']})
    result = []
    for r in reqs:
        r['_id'] = str(r['_id'])
        r['owner_id'] = str(r['owner_id'])
        r['walker_id'] = str(r['walker_id'])
        r['ad_id'] = str(r['ad_id'])
        r['dogs'] = [str(d) for d in r['dogs']]
        result.append(r)
    return jsonify(result), 200

@requests_bp.route('/walker', methods=['GET'])
@jwt_required()
@role_required('walker')
def get_walker_requests():
    current_email = get_jwt_identity()
    walker = get_user_by_email(current_email)
    if not walker:
        return jsonify({"msg": "Walker no encontrado"}), 404

    reqs = mongo.db.requests.find({"walker_id": walker['_id']})
    result = []
    for r in reqs:
        r['_id'] = str(r['_id'])
        r['owner_id'] = str(r['owner_id'])
        r['walker_id'] = str(r['walker_id'])
        r['ad_id'] = str(r['ad_id'])
        r['dogs'] = [str(d) for d in r['dogs']]
        result.append(r)
    return jsonify(result), 200

@requests_bp.route('/<request_id>/accept', methods=['PATCH'])
@jwt_required()
@role_required('walker')
def accept_request(request_id):
    current_email = get_jwt_identity()
    walker = get_user_by_email(current_email)
    req = mongo.db.requests.find_one({"_id": ObjectId(request_id), "walker_id": walker['_id']})
    if not req:
        return jsonify({"msg": "Solicitud no encontrada"}), 404
    if req['status'] != 'pendiente':
        return jsonify({"msg": "Solo puedes aceptar solicitudes pendientes"}), 400
    mongo.db.requests.update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "aceptada"}})
    return jsonify({"msg": "Solicitud aceptada"}), 200

@requests_bp.route('/<request_id>/reject', methods=['PATCH'])
@jwt_required()
@role_required('walker')
def reject_request(request_id):
    current_email = get_jwt_identity()
    walker = get_user_by_email(current_email)
    req = mongo.db.requests.find_one({"_id": ObjectId(request_id), "walker_id": walker['_id']})
    if not req:
        return jsonify({"msg": "Solicitud no encontrada"}), 404
    if req['status'] != 'pendiente':
        return jsonify({"msg": "Solo puedes rechazar solicitudes pendientes"}), 400
    mongo.db.requests.update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "rechazada"}})
    return jsonify({"msg": "Solicitud rechazada"}), 200

@requests_bp.route('/<request_id>/cancel', methods=['PATCH'])
@jwt_required()
def cancel_request(request_id):
    current_email = get_jwt_identity()
    req = mongo.db.requests.find_one({"_id": ObjectId(request_id)})
    if not req:
        return jsonify({"msg": "Solicitud no encontrada"}), 404

    user = get_user_by_email(current_email)
    if user['_id'] == req['owner_id']:
        mongo.db.requests.update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "cancelada_por_owner"}})
        return jsonify({"msg": "Solicitud cancelada por el dueño"}), 200
    elif user['_id'] == req['walker_id']:
        mongo.db.requests.update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "cancelada_por_walker"}})
        return jsonify({"msg": "Solicitud cancelada por el paseador"}), 200
    else:
        return jsonify({"msg": "No autorizado"}), 403