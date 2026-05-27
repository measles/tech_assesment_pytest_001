"""Tests for findings (scan results)."""

import httpx

from tech_assesment_001.utils.logger import log_api_response


def test_user_regardless_of_role_can_read_findings(
    base_url, admin_alpha_token, user_alpha_token
):
    """
    Test that both admin and regular users can read findings (scan results).
    (Checklist items 11, 12)
    """
    # 1. Administrator reads findings (Item 11)
    with httpx.Client(base_url=base_url) as client:
        admin_res = client.get(
            "/findings",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(admin_res.request, admin_res)

    assert (
        admin_res.status_code == 200
    ), f"Expected 200 OK for admin, but got {admin_res.status_code}"
    admin_data = admin_res.json()
    assert "items" in admin_data, "Admin response missing 'items' field"
    assert isinstance(
        admin_data["items"], list
    ), "'items' field in admin response is not a list"

    # 2. Regular user reads findings (Item 12)
    with httpx.Client(base_url=base_url) as client:
        user_res = client.get(
            "/findings",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(user_res.request, user_res)

    assert (
        user_res.status_code == 200
    ), f"Expected 200 OK for user, but got {user_res.status_code}"
    user_data = user_res.json()
    assert "items" in user_data, "User response missing 'items' field"
    assert isinstance(
        user_data["items"], list
    ), "'items' field in user response is not a list"
