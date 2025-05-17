from flask import Flask
from dotenv import load_dotenv
import os

from extensions import mongo, bcrypt, jwt
from resources.auth import auth_bp
from resources.dogs import dogs_bp
from resources.advertisements import advertisements_bp
from flask_cors import CORS


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["BCRYPT_LOG_ROUNDS"] = 4

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dogs_bp)
    app.register_blueprint(advertisements_bp)

    CORS(app)

    @app.route('/')
    def home():
        return "API DogGo funcionando!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)