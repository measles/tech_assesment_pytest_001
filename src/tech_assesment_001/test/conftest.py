"""Shared test fixtures for the tech assessment tests."""
import pytest


@pytest.fixture
def base_url():
    """Returns the base URL for the API."""
    return "http://54.226.15.13:8000"
