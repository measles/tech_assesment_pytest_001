"""Tests for findings (scan results)."""

import httpx

from tech_assesment_001.utils.logger import log_api_response


def test_admin_can_read_findings(base_url, admin_alpha_token):
    """
    Test that an administrator can successfully read findings (scan results).
    (Checklist item 11)
    """
    with httpx.Client(base_url=base_url) as client:
        response = client.get(
            "/findings",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(response.request, response)

    assert (
        response.status_code == 200
    ), f"Expected 200 OK for admin findings access, but got {response.status_code}"
    data = response.json()
    assert "items" in data, "Admin findings response missing 'items' field"
    assert isinstance(
        data["items"], list
    ), "'items' field in admin findings response is not a list"


def test_user_can_read_findings(base_url, user_alpha_token):
    """
    Test that a regular user can successfully read findings (scan results).
    (Checklist item 12)
    """
    with httpx.Client(base_url=base_url) as client:
        response = client.get(
            "/findings",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(response.request, response)

    assert (
        response.status_code == 200
    ), f"Expected 200 OK for user findings access, but got {response.status_code}"
    data = response.json()
    assert "items" in data, "User findings response missing 'items' field"
    assert isinstance(
        data["items"], list
    ), "'items' field in user findings response is not a list"
