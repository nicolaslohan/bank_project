from flask import Blueprint, request, jsonify
from backend.models import BankUser, Banks, UserProfiles, db
from werkzeug.security import generate_password_hash

bank_users_bp = Blueprint("bank_users", __name__)


@bank_users_bp.route("/create", methods=["POST"])
def create_bank_user():
    """
    Endpoint to create a new bank user.
    """
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    if "profile_id" not in data or "bank_id" not in data:
        return jsonify({"error": "Profile ID and Bank ID are required"}), 400

    # Verifica se o username já existe
    user = BankUser.query.filter_by(username=data["username"], status=True).first()
    if user:
        return jsonify({"error": "Username already exists"}), 400

    # Verifica se o banco existe
    bank = Banks.query.filter_by(id=data["bank_id"]).first()
    print(f"Bank ID {data['bank_id']} found: {bank}")
    banks = Banks.query.all()
    print("Available bank IDs:", [b.id for b in banks])
    if not bank:
        return jsonify({"error": "Banco não encontrado"}), 400

    # Verifica se o perfil existe
    profile = UserProfiles.query.get(data["profile_id"])
    if not profile:
        return jsonify({"error": "Perfil não encontrado"}), 400

    new_user = BankUser(
        username=data["username"],
        password=generate_password_hash(data["password"]),
        profile_id=data["profile_id"],
        bank_id=data["bank_id"],
        status=True,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@bank_users_bp.route("/all", methods=["GET"])
def get_bank_users():
    """
    Endpoint to retrieve all bank users.
    """
    bank_users = BankUser.query.filter_by(status=True).all()
    return (
        jsonify([bank_user.to_dict() for bank_user in bank_users]),
        200,
    )


@bank_users_bp.route("/<int:user_id>", methods=["GET"])
def get_bank_user(user_id):
    """
    Endpoint to retrieve a specific bank user by ID.
    """
    user = BankUser.query.get(user_id)
    if not user or not user.status:
        return jsonify({"error": "User not found"}), 404

    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "profile_id": user.profile_id,
                "bank_id": user.bank_id,
                "status": user.status,
            }
        ),
        200,
    )


@bank_users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_bank_user(user_id):
    """
    Endpoint to delete a specific bank user by ID.
    """
    user = BankUser.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200
