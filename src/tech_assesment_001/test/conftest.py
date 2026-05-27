"""Shared test fixtures and hooks for the tech assessment tests."""

import pytest
from pytest_html import extras  # type: ignore[import-untyped]

from tech_assesment_001.utils.auth import get_tokens
from tech_assesment_001.utils.credentials import load_credentials

# Global cache for tokens to avoid 429 Too Many Requests
TOKEN_CACHE: dict[str, str] = {}


@pytest.fixture(scope="session")
def base_url():
    """Returns the base URL for the API."""
    return "http://54.226.15.13:8000"


@pytest.fixture(autouse=True)
def setup_api_logging(caplog):
    """Automatically set the api_test logger level for all tests."""
    caplog.set_level("INFO", logger="api_test")


@pytest.fixture(scope="session")
def auth_tokens(base_url):  # pylint: disable=redefined-outer-name
    """
    Session-scoped fixture to provide cached authentication tokens.
    Returns a function that takes email and password and returns a token.
    """

    def _get_cached_token(email, password):
        if email not in TOKEN_CACHE:
            token, _ = get_tokens(base_url, email, password)
            TOKEN_CACHE[email] = token
        return TOKEN_CACHE[email]

    return _get_cached_token


@pytest.fixture
def admin_alpha_token(auth_tokens):  # pylint: disable=redefined-outer-name
    """Fixture to provide the admin token for org-alpha."""
    orgs = load_credentials()
    admin_creds = orgs["org-alpha"].admin
    assert admin_creds, "Admin credentials for org-alpha not found"
    return auth_tokens(admin_creds.email, admin_creds.password)


@pytest.fixture
def user_alpha_token(auth_tokens):  # pylint: disable=redefined-outer-name
    """Fixture to provide the user token for org-alpha."""
    orgs = load_credentials()
    user_creds = orgs["org-alpha"].user
    assert user_creds, "User credentials for org-alpha not found"
    return auth_tokens(user_creds.email, user_creds.password)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture logs and add them to the HTML report.
    """
    # pylint: disable=unused-argument
    outcome = yield
    report = outcome.get_result()

    if report.when in ("call", "teardown"):
        # Capture logs from the 'caplog' fixture if available
        caplog = item.funcargs.get("caplog")
        if caplog:
            try:
                log_content = caplog.text
                if log_content:
                    if not hasattr(report, "extras"):
                        report.extras = []
                    # Distinguish between call and teardown logs
                    name = "API Logs" if report.when == "call" else "Teardown API Logs"
                    report.extras.append(extras.text(log_content, name=name))
            except (KeyError, AttributeError):
                # caplog might not be available or its stash key might be missing during some phases
                pass
