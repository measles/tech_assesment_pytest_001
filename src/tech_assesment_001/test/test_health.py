"""Tests for health check endpoint."""

import httpx

from tech_assesment_001.utils.logger import log_api_response


def test_health_check_unauthenticated(base_url):
    """
    Test that the health check endpoint is accessible without authentication.
    (Checklist item 18)
    """
    with httpx.Client(base_url=base_url) as client:
        response = client.get("/health")
        log_api_response(response.request, response)

    assert (
        response.status_code == 200
    ), f"Expected 200 OK for unauthenticated health check, but got {response.status_code}"
    data = response.json()
    assert "status" in data, "Health check response missing 'status' field"
    assert (
        data["status"] == "ok"
    ), f"Expected status 'ok', but got '{data.get('status')}'"
