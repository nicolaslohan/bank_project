from flask import Blueprint, request, jsonify
from backend.models import ClientUser, BankUser, db
from werkzeug.security import generate_password_hash

register_bp = Blueprint("register", __name__)


@register_bp.route("/user", methods=["POST"])
def register_user():
    data = request.json
    if (
        not data
        or "username" not in data
        or "password" not in data
        or "profile_id" not in data
    ):
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]
    profile_id = data.get("profile_id", 1)

    user = BankUser.query.filter_by(username=username).first()
    if user:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = BankUser(
        username=username, password=hashed_password, status=True, profile_id=profile_id
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@register_bp.route("/client", methods=["POST"])
def register_client():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    user = ClientUser.query.filter_by(username=username).first()
    if user:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = ClientUser(
        username=username, password=hashed_password, status=True, description="Created"
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
