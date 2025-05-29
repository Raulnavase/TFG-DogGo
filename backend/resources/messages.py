from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId
from datetime import datetime

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/messages/<user_id>', methods=['GET'])
@jwt_required()
def get_messages(user_id):
    user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    my_id = str(user["_id"])
    other_id = user_id

    messages = list(mongo.db.messages.find({
        "$or": [
            {"owner_id": my_id, "walker_id": other_id},
            {"owner_id": other_id, "walker_id": my_id}
        ]
    }).sort("timestamp", 1))

    formatted = [
        {
            "id": str(msg["_id"]),
            "text": msg["text"],
            "sent": msg["sender_id"] == my_id,
            "timestamp": msg["timestamp"]
        }
        for msg in messages
    ]
    return jsonify(formatted), 200

@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    data = request.get_json()
    walker_id = data.get("walkerId")
    text = data.get("text")
    owner_id = data.get("ownerId")

    if not walker_id or not text:
        return jsonify({"msg": "Faltan datos"}), 400

    if user["role"] == "owner":
        owner_id = str(user["_id"])
        sender_id = owner_id
    else:
        sender_id = str(user["_id"])
        if not owner_id:
            return jsonify({"msg": "Falta ownerId"}), 400

    message = {
        "owner_id": owner_id,
        "walker_id": walker_id,
        "sender_id": sender_id,
        "text": text,
        "timestamp": datetime.utcnow().isoformat()
    }
    result = mongo.db.messages.insert_one(message)
    message["id"] = str(result.inserted_id)
    return jsonify({
        "msg": "Mensaje enviado",
        "message": {
            "id": message["id"],
            "text": message["text"],
            "sent": True,
            "timestamp": message["timestamp"]
        }
    }), 201


@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_email = get_jwt_identity()
    user = mongo.db.users.find_one({"email": user_email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    user_id = str(user["_id"])
    role = user["role"]

    if role == "owner":
        pipeline = [
            {"$match": {"owner_id": user_id}},
            {"$group": {"_id": "$walker_id"}},
            {"$addFields": {"walkerObjId": {"$toObjectId": "$_id"}}},
            {"$lookup": {
                "from": "users",
                "localField": "walkerObjId",
                "foreignField": "_id",
                "as": "walker"
            }},
            {"$unwind": "$walker"},
            {"$project": {"id": "$_id", "name": "$walker.name"}}
        ]
    else:
        pipeline = [
            {"$match": {"walker_id": user_id}},
            {"$group": {"_id": "$owner_id"}},
            {"$addFields": {"ownerObjId": {"$toObjectId": "$_id"}}},
            {"$lookup": {
                "from": "users",
                "localField": "ownerObjId",
                "foreignField": "_id",
                "as": "owner"
            }},
            {"$unwind": "$owner"},
            {"$project": {"id": "$_id", "name": "$owner.name"}}
        ]
    conversations = list(mongo.db.messages.aggregate(pipeline))
    return jsonify(conversations), 200