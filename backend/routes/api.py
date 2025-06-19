from flask import Blueprint, request, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.oauth2.rfc6750 import BearerTokenValidator
from backend.models import SessionToken, ClientUser, BankUser, UserProfiles, Banks

api_bp = Blueprint("api", __name__)
require_oauth = ResourceProtector()


class TokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        token = SessionToken.query.filter_by(token=token_string, revoked=False).first()
        return token

    def request_invalid(self, request):
        return not request.headers.get("Authorization", "").startswith("Bearer ")

    def token_revoked(self, token):
        token.revoke_if_expired()
        return token.is_revoked()


require_oauth.register_token_validator(TokenValidator())


@api_bp.route("/me")
@require_oauth("profile")
def me():
    token = current_token
    user = BankUser.query.get(token.get_user_id())
    profile = UserProfiles.query.get(user.profile_id)
    bank = Banks.query.get(user.bank_id)
    return (
        jsonify(
            {
                "username": user.username,
                "profile": profile.title,
                "bank": "" if not bank else bank.name,
            }
        ),
        200,
    )
