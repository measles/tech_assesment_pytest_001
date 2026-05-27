"""Logging utilities for API tests using Python's built-in logging module."""

import json
import logging

import httpx

logger = logging.getLogger("api_test")


def mask_sensitive_data(data):
    """
    Recursively replaces values of keys named 'password' with '***'.
    """
    if isinstance(data, dict):
        return {
            k: ("***" if k.lower() == "password" else mask_sensitive_data(v))
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [mask_sensitive_data(item) for item in data]
    return data


def log_api_response(request: httpx.Request, response: httpx.Response):
    """
    Formats and logs the API request and response with sensitive data masked.
    """
    try:
        req_body = request.read().decode("utf-8")
        if req_body:
            data = json.loads(req_body)
            masked_data = mask_sensitive_data(data)
            req_body = json.dumps(masked_data, indent=2)
    except (json.JSONDecodeError, UnicodeDecodeError):
        req_body = "<binary or non-json data>"

    try:
        data = response.json()
        masked_data = mask_sensitive_data(data)
        res_body = json.dumps(masked_data, indent=2)
    except (json.JSONDecodeError, httpx.HTTPError):
        res_body = response.text

    log_entry = (
        f"\nURL: {request.method} {request.url}\n"
        f"Request Body:\n{req_body}\n"
        f"Response Status: {response.status_code}\n"
        f"Response Body:\n{res_body}"
    )
    logger.info(log_entry)
