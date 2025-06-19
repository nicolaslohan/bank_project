from authlib.oauth2.rfc6749 import grants
from backend.models import ClientUser, BankUser
from werkzeug.security import check_password_hash


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = ClientUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        user = BankUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        return None
