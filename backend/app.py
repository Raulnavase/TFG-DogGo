from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from extensions import mongo, bcrypt, jwt
from resources.auth import auth_bp
from resources.dogs import dogs_bp
from resources.advertisements import advertisements_bp
from resources.requests import requests_bp
from resources.users import users_bp
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from functools import wraps

def create_app():
    load_dotenv()

    app = Flask(__name__)

    CORS(app, supports_credentials=True, origins=["https://tfg-dog-go.vercel.app"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization", "X-API-Key"])

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["BCRYPT_LOG_ROUNDS"] = 12
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

    Talisman(app, force_https=True, strict_transport_security=True, session_cookie_secure=True)

    def require_api_key(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            if api_key and api_key == os.getenv("API_KEY"):
                return f(*args, **kwargs)
            return jsonify({"msg": "Clave API inválida"}), 401
        return decorated

    app.register_blueprint(auth_bp)
    app.register_blueprint(dogs_bp)
    app.register_blueprint(advertisements_bp)
    app.register_blueprint(requests_bp)
    app.register_blueprint(users_bp)

    @app.route('/')
    @require_api_key
    def home():
        return jsonify({"msg": "API DogGo funcionando!"})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"msg": "Recurso no encontrado"}), 404

    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify({"msg": "Límite de solicitudes excedido"}), 429

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', ssl_context='adhoc')