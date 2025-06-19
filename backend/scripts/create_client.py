from backend.models import db, OAuth2Client
from backend.app import app

with app.app_context():
    client = OAuth2Client(
        client_id="client-app",
        client_secret="client-secret",
        client_name="Aplicativo Cliente",
    )

    # Atribuindo todos os metadados de uma vez
    client.set_client_metadata(
        {
            "token_endpoint_auth_method": "client_secret_basic",
            "grant_types": [
                "password"
            ],  # ou ["password"], ["authorization_code"], etc.
            "response_types": ["token"],  # ou ["code"]
            "scope": "profile",
            "redirect_uris": [],  # vazio se não usar code flow
        }
    )

    db.session.add(client)
    db.session.commit()
    print("✅ Client OAuth registrado com sucesso:")
    print(f"   client_id:     {client.client_id}")
    print(f"   client_secret: {client.client_secret}")

    # client = OAuth2Client.query.filter_by(client_id="client-app").first()
    # if client:
    #     db.session.delete(client)
    #     db.session.commit()
    #     print("✅ Client OAuth removido com sucesso:")
