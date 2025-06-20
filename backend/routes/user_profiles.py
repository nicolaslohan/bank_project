from flask import Blueprint, request, jsonify
from backend.models import db, UserProfiles

user_profiles_bp = Blueprint("user_profiles", __name__)


@user_profiles_bp.route("/create", methods=["POST"])
def create_user_profile():
    """
    Endpoint to create a new user profile.
    """
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    existing_profile = UserProfiles.query.filter_by(
        title=data["title"], status=True
    ).first()
    if existing_profile:
        return jsonify({"error": "Profile already exists"}), 400

    new_profile = UserProfiles(title=data["title"], status=True)
    db.session.add(new_profile)
    db.session.commit()

    return (
        jsonify({"id": new_profile.id, "title": new_profile.title}),
        201,
    )


@user_profiles_bp.route("/all", methods=["GET"])
def get_user_profiles():
    profiles = UserProfiles.query.filter_by(status=True).all()
    return (
        jsonify([{"id": profile.id, "title": profile.title} for profile in profiles]),
        200,
    )
