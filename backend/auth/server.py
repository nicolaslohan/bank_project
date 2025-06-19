from authlib.integrations.flask_oauth2 import AuthorizationServer
from backend.auth.tokens import save_token
from backend.models import db, OAuth2Client
from backend.auth.grant_types import PasswordGrant

authorization = AuthorizationServer(save_token=save_token)


def configure_oauth(app):
    authorization.init_app(
        app,
        query_client=lambda client_id: OAuth2Client.query.filter_by(
            client_id=client_id
        ).first(),
    )
    authorization.register_grant(PasswordGrant)
