"""Shared test fixtures and hooks for the tech assessment tests."""

import pytest
from pytest_html import extras


@pytest.fixture
def base_url():
    """Returns the base URL for the API."""
    return "http://54.226.15.13:8000"


@pytest.fixture(autouse=True)
def setup_api_logging(caplog):
    """Automatically set the api_test logger level for all tests."""
    caplog.set_level("INFO", logger="api_test")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture logs and add them to the HTML report.
    """
    # pylint: disable=unused-argument
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Capture logs from the 'caplog' fixture if available
        caplog = item.funcargs.get("caplog")
        if caplog:
            log_content = caplog.text
            if log_content:
                if not hasattr(report, "extras"):
                    report.extras = []
                report.extras.append(extras.text(log_content, name="API Logs"))
