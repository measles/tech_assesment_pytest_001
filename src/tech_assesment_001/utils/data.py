"""Utility functions for test data generation."""

from datetime import datetime


def generate_timestamped_name(base_name: str) -> str:
    """
    Generates a randomized name using a timestamp.
    Format: "Base Name HH:MM:SS.ffffffTDD-MM-YYYY"
    """
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S.%f")[:-1] + "T" + now.strftime("%d-%m-%Y")
    return f"{base_name} {timestamp}"
