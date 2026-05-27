"""Tests for authentication and authorization."""
import httpx

from tech_assesment_001.utils.credentials import load_credentials


def test_authorization_returns_tokens(base_url):
    """
    Test that a successful login returns an access token and a refresh token.
    (Checklist item 1)
    """
    orgs = load_credentials()
    assert "org-alpha" in orgs

    admin_creds = orgs["org-alpha"].admin
    assert admin_creds, "Admin credentials for org-alpha not found"

    email = admin_creds.email
    password = admin_creds.password

    with httpx.Client(base_url=base_url) as client:
        response = client.post(
            "/auth/login",
            json={"email": email, "password": password}
        )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
