from backend.models import SessionToken, db
from datetime import datetime, timedelta
import secrets


def save_token(token_data, request):
    token = token_data.get("access_token")
    expires = datetime.utcnow() + timedelta(seconds=token_data.get("expires_in", 3600))
    user = request.user
    session = SessionToken(
        token=token,
        created_at=datetime.utcnow(),
        expires_at=expires,
        revoked=False,
        user_id=(getattr(user, "id", None) if hasattr(user, "username") else None),
        scope=token_data.get("scope", ""),
        user_agent=(
            request.headers.get("User-Agent") if hasattr(request, "headers") else None
        ),
    )

    db.session.add(session)
    db.session.commit()
