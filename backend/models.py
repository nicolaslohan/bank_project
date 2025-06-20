from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

db = SQLAlchemy()


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = "oauth2_clients"
    id = db.Column(db.BigInteger, primary_key=True)
    client_name = db.Column(db.String, nullable=False, unique=True)


class ClientUser(db.Model):
    __tablename__ = "client_users"
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    description = db.Column(db.String, nullable=True)


class BankUser(db.Model):
    __tablename__ = "bank_users"
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, default=True)
    bank_id = db.Column(db.BigInteger, db.ForeignKey("banks.id"), nullable=False)
    profile_id = db.Column(
        db.BigInteger, db.ForeignKey("user_profiles.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String, nullable=True)

    bank = db.relationship("Banks", back_populates="users", foreign_keys=[bank_id])
    profile = db.relationship(
        "UserProfiles", back_populates="users", foreign_keys=[profile_id]
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "status": self.status,
            "bank_id": self.bank_id,
            "profile_id": self.profile_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "description": self.description,
            "bank": (
                {
                    "id": self.bank.id,
                    "name": self.bank.name,
                    "status": self.bank.status,
                    "created_at": (
                        self.bank.created_at.isoformat()
                        if self.bank.created_at
                        else None
                    ),
                }
                if self.bank
                else {
                    "id": 0,
                    "name": "Sem informação",
                    "status": False,
                    "created_at": None,
                }
            ),
            "profile": (
                {
                    "id": self.profile.id,
                    "title": self.profile.title,
                    "permissions": self.profile.permissions,
                    "status": self.profile.status,
                    "created_at": (
                        self.profile.created_at.isoformat()
                        if self.profile.created_at
                        else None
                    ),
                }
                if self.profile
                else {
                    "id": 0,
                    "title": "Sem informação",
                    "permissions": None,
                    "status": False,
                    "created_at": None,
                }
            ),
        }


class SessionToken(db.Model):
    __tablename__ = "session_tokens"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    token = db.Column(db.String, nullable=False)
    user_agent = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    revoked = db.Column(db.Boolean, default=False)
    scope = db.Column(db.String, nullable=True)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def revoke_if_expired(self):
        if self.is_expired():
            self.revoked = True
            db.session.commit()

    def is_revoked(self):
        return self.revoked

    def get_scope(self):
        return self.scope

    def get_user_id(self):
        return self.user_id

    def get_user_type(self):
        return self.user_type

    @property
    def user(self):
        return (
            ClientUser.query.get(self.user_id)
            if self.user_type == 1
            else BankUser.query.get(self.user_id)
        )


class Banks(db.Model):
    __tablename__ = "banks"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)

    users = db.relationship("BankUser", back_populates="bank")


class UserProfiles(db.Model):
    __tablename__ = "user_profiles"
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String, nullable=False)
    permissions = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)

    users = db.relationship("BankUser", back_populates="profile")
