from flask import Flask
from flask_cors import CORS
from .models import db
from .auth.server import configure_oauth
from .routes.oauth import oauth_bp
from .routes.api import api_bp
from .routes.user_profiles import user_profiles_bp
from .routes.register import register_bp
from .routes.banks import bank_bp
from .routes.bank_users import bank_users_bp

import os
import dotenv

dotenv.load_dotenv()


def create_app():

    app = Flask(__name__)

    CORS(app, origins=["http://localhost:5173"])

    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_DATABASE_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    configure_oauth(app)

    app.register_blueprint(oauth_bp, url_prefix="/oauth")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(user_profiles_bp, url_prefix="/user_profiles")
    app.register_blueprint(register_bp, url_prefix="/register")
    app.register_blueprint(bank_bp, url_prefix="/banks")
    app.register_blueprint(bank_users_bp, url_prefix="/bank_users")

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

    return app


if __name__ == "__main__":
    backend = create_app()
    backend.run(debug=True)
