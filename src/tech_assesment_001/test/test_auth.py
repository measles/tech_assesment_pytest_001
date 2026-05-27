"""Tests for authentication and authorization."""

from tech_assesment_001.utils.auth import get_tokens
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

    access_token, refresh_token = get_tokens(base_url, email, password)

    assert access_token, "Access token is missing in the login response"
    assert refresh_token, "Refresh token is missing in the login response"
