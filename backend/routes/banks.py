from flask import Blueprint, request, jsonify
from backend.models import Banks, db

bank_bp = Blueprint("bank", __name__)


@bank_bp.route("/create", methods=["POST"])
def create_bank():
    """
    Endpoint to create a new bank.
    """
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Bank name is required"}), 400

    bank_name = data["name"]
    existing_bank = Banks.query.filter_by(name=bank_name, status=True).first()
    if existing_bank:
        return jsonify({"error": "Bank already exists"}), 400

    new_bank = Banks(name=bank_name, status=True)
    db.session.add(new_bank)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_bank.id,
                "name": new_bank.name,
                "created_at": new_bank.created_at,
                "status": new_bank.status,
            }
        ),
        201,
    )


@bank_bp.route("/all", methods=["GET"])
def get_banks():
    """
    Endpoint to retrieve all banks.
    """
    banks = Banks.query.filter_by(status=True).all()
    print(f"Retrieved {len(banks)} banks from the database.")
    return (
        jsonify(
            [
                {
                    "id": bank.id,
                    "name": bank.name,
                    "created_at": bank.created_at,
                    "status": bank.status,
                }
                for bank in banks
            ]
        ),
        200,
    )


@bank_bp.route("/<int:bank_id>", methods=["GET"])
def get_bank(bank_id):
    """
    Endpoint to retrieve a specific bank by ID.
    """
    bank = Banks.query.get(bank_id)
    if not bank or not bank.status:
        return jsonify({"error": "Bank not found"}), 404

    return (
        jsonify(
            {
                "id": bank.id,
                "name": bank.name,
                "created_at": bank.created_at,
                "status": bank.status,
            }
        ),
        200,
    )


@bank_bp.route("/<int:bank_id>", methods=["DELETE"])
def delete_bank(bank_id):
    """
    Endpoint to delete a bank by ID.
    """
    bank = Banks.query.get(bank_id)
    if not bank or not bank.status:
        return jsonify({"error": "Bank not found"}), 404

    bank.status = False
    db.session.commit()

    return jsonify({"message": "Bank deleted successfully"}), 200


@bank_bp.route("/<int:bank_id>", methods=["PUT"])
def update_bank(bank_id):
    """
    Endpoint to update a bank's name by ID.
    """
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Bank name is required"}), 400

    bank = Banks.query.get(bank_id)
    if not bank or not bank.status:
        return jsonify({"error": "Bank not found"}), 404

    bank.name = data["name"]
    db.session.commit()

    return (
        jsonify(
            {
                "id": bank.id,
                "name": bank.name,
                "created_at": bank.created_at,
                "status": bank.status,
            }
        ),
        200,
    )
