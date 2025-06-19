from flask import Blueprint, request
from backend.auth.server import authorization

oauth_bp = Blueprint("oauth", __name__)


@oauth_bp.route("/token", methods=["POST"])
def issue_token():
    """
    Endpoint to issue OAuth tokens.
    """
    return authorization.create_token_response()
