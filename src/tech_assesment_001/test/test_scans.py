"""Tests for scan management."""

import httpx

from tech_assesment_001.utils.logger import log_api_response


def test_admin_can_create_scan_and_status_is_readable(
    base_url, admin_alpha_token, user_alpha_token
):
    """
    Test that an administrator can create a scan and both admin and user can read its status.
    (Checklist items 9, 17, 18)
    """
    # 1. Administrator starts a scan (Item 9)
    with httpx.Client(base_url=base_url) as client:
        start_res = client.post(
            "/scans",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(start_res.request, start_res)

    assert (
        start_res.status_code == 200
    ), f"Expected 200 OK for scan creation, but got {start_res.status_code}"
    data = start_res.json()
    assert "scan_id" in data, "Scan creation response missing 'scan_id' field"
    assert (
        data["status"] == "IN_PROGRESS"
    ), f"Expected status 'IN_PROGRESS', but got {data.get('status')}"
    scan_id = data["scan_id"]

    # 2. Administrator reads the scan status (Item 17)
    with httpx.Client(base_url=base_url) as client:
        admin_status_res = client.get(
            f"/scans/{scan_id}/status",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(admin_status_res.request, admin_status_res)

    assert (
        admin_status_res.status_code == 200
    ), f"Expected 200 OK for admin status check, but got {admin_status_res.status_code}"
    admin_data = admin_status_res.json()
    assert admin_data["id"] == scan_id, "Admin status response returned wrong scan ID"
    assert admin_data["status"] in (
        "IN_PROGRESS",
        "COMPLETED",
        "FAILED",
    ), f"Unexpected scan status: {admin_data.get('status')}"

    # 3. Regular user reads the scan status (Item 18)
    with httpx.Client(base_url=base_url) as client:
        user_status_res = client.get(
            f"/scans/{scan_id}/status",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(user_status_res.request, user_status_res)

    assert (
        user_status_res.status_code == 200
    ), f"Expected 200 OK for user status check, but got {user_status_res.status_code}"
    user_data = user_status_res.json()
    assert user_data["id"] == scan_id, "User status response returned wrong scan ID"
    assert user_data["status"] in (
        "IN_PROGRESS",
        "COMPLETED",
        "FAILED",
    ), f"Unexpected scan status: {user_data.get('status')}"


def test_user_cannot_create_scan(base_url, user_alpha_token):
    """
    Test that a regular user cannot start a discovery scan.
    (Checklist item 10)
    """
    with httpx.Client(base_url=base_url) as client:
        response = client.post(
            "/scans",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(response.request, response)

    assert response.status_code == 403, "User can start the scan while shouldn't"
