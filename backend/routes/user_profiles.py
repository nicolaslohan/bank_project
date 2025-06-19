from flask import Blueprint, request, jsonify
from backend.models import db, UserProfiles

user_profiles_bp = Blueprint("user_profiles", __name__)


@user_profiles_bp.route("/all", methods=["GET"])
def get_user_profiles():
    profiles = UserProfiles.query.filter_by(status=True).all()
    return (
        jsonify([{"id": profile.id, "title": profile.title} for profile in profiles]),
        200,
    )
