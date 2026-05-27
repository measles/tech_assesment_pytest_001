"""Tests for asset management."""

import httpx

from tech_assesment_001.utils.auth import get_tokens
from tech_assesment_001.utils.credentials import load_credentials
from tech_assesment_001.utils.logger import log_api_response


def test_user_regardless_of_role_can_read_assets(base_url):
    """
    Test that both admin and regular users can read the asset list.
    (Checklist item 2)
    """
    orgs = load_credentials()
    assert "org-alpha" in orgs
    org_alpha = orgs["org-alpha"]

    # 1. Test as Admin
    admin_creds = org_alpha.admin
    assert admin_creds, "Admin credentials for org-alpha not found"
    admin_token, _ = get_tokens(base_url, admin_creds.email, admin_creds.password)

    with httpx.Client(base_url=base_url) as client:
        admin_response = client.get(
            "/assets", headers={"Authorization": f"Bearer {admin_token}"}
        )
        log_api_response(admin_response.request, admin_response)
    assert admin_response.status_code == 200

    # 2. Test as Regular User
    user_creds = org_alpha.user
    assert user_creds, "User credentials for org-alpha not found"
    user_token, _ = get_tokens(base_url, user_creds.email, user_creds.password)

    with httpx.Client(base_url=base_url) as client:
        user_response = client.get(
            "/assets", headers={"Authorization": f"Bearer {user_token}"}
        )
        log_api_response(user_response.request, user_response)
    assert user_response.status_code == 200

    # Basic validation of response structure
    admin_data = admin_response.json()
    user_data = user_response.json()

    assert "items" in admin_data
    assert isinstance(admin_data["items"], list)
    assert "items" in user_data
    assert isinstance(user_data["items"], list)
