"""Tests for security reports."""

import httpx

from tech_assesment_001.utils.logger import log_api_response


def test_admin_can_read_report(base_url, admin_alpha_token):
    """
    Test that an administrator can successfully read the report summary.
    (Checklist item 13)
    """
    with httpx.Client(base_url=base_url) as client:
        response = client.get(
            "/reports/summary",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(response.request, response)

    assert (
        response.status_code == 200
    ), f"Expected 200 OK for admin report access, but got {response.status_code}"
    data = response.json()
    assert (
        "risk_score_percent" in data
    ), "Admin report response missing 'risk_score_percent' field"
    assert "total_assets" in data, "Admin report response missing 'total_assets' field"


def test_user_can_read_report(base_url, user_alpha_token):
    """
    Test that a regular user can successfully read the report summary.
    (Checklist item 14)
    """
    with httpx.Client(base_url=base_url) as client:
        response = client.get(
            "/reports/summary",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(response.request, response)

    assert (
        response.status_code == 200
    ), f"Expected 200 OK for user report access, but got {response.status_code}"
    data = response.json()
    assert (
        "risk_score_percent" in data
    ), "User report response missing 'risk_score_percent' field"
    assert "total_assets" in data, "User report response missing 'total_assets' field"
