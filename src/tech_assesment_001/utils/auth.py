"""Authentication utilities for testing."""

import httpx

from tech_assesment_001.utils.logger import log_api_response


def get_tokens(base_url, email, password):
    """
    Performs login and returns the access and refresh tokens.
    """
    with httpx.Client(base_url=base_url) as client:
        response = client.post(
            "/auth/login", json={"email": email, "password": password}
        )
        log_api_response(response.request, response)
        response.raise_for_status()
        data = response.json()
        return data["access_token"], data["refresh_token"]
