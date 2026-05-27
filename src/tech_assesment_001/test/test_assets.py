"""Tests for asset management."""

import httpx
import pytest

from tech_assesment_001.utils.data import generate_timestamped_name
from tech_assesment_001.utils.logger import log_api_response


@pytest.fixture
def test_asset(base_url, admin_alpha_token):  # pylint: disable=redefined-outer-name
    """
    Fixture to create a single asset as admin and delete it after the test.
    Yields the asset data dictionary.
    """
    asset_name = generate_timestamped_name("Test Asset")
    payload = {
        "name": asset_name,
        "asset_type": "EC2",
        "cloud_account": "123456789",
        "region": "us-east-1",
        "tags": {"environment": "test"},
    }

    with httpx.Client(base_url=base_url) as client:
        response = client.post(
            "/assets",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
            json=payload,
        )
        log_api_response(response.request, response)

    assert response.status_code in (
        200,
        201,
    ), f"Fixture failed to create asset: expected 200/201, got {response.status_code}"
    asset_data = response.json()
    asset_id = asset_data["id"]

    yield asset_data

    # Teardown: delete the created asset
    with httpx.Client(base_url=base_url) as client:
        response = client.delete(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(response.request, response)


def test_user_regardless_of_role_can_read_assets(
    base_url, admin_alpha_token, user_alpha_token
):  # pylint: disable=redefined-outer-name
    """
    Test that both admin and regular users can read the asset list.
    (Checklist item 2)
    """
    # 1. Test as Admin
    with httpx.Client(base_url=base_url) as client:
        admin_response = client.get(
            "/assets",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(admin_response.request, admin_response)
    assert (
        admin_response.status_code == 200
    ), f"Admin expected 200 OK for asset list, got {admin_response.status_code}"

    # 2. Test as Regular User
    with httpx.Client(base_url=base_url) as client:
        user_response = client.get(
            "/assets",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(user_response.request, user_response)
    assert (
        user_response.status_code == 200
    ), f"User expected 200 OK for asset list, got {user_response.status_code}"

    # Basic validation of response structure
    admin_data = admin_response.json()
    user_data = user_response.json()

    assert "items" in admin_data, "Admin response missing 'items' field"
    assert isinstance(
        admin_data["items"], list
    ), "'items' field in admin response is not a list"
    assert "items" in user_data, "User response missing 'items' field"
    assert isinstance(
        user_data["items"], list
    ), "'items' field in user response is not a list"


def test_admin_can_create_asset(test_asset):  # pylint: disable=redefined-outer-name
    """
    Test that an administrator can successfully create an asset.
    (Checklist item 3)
    """
    assert "id" in test_asset, "Created asset missing 'id' field"
    assert test_asset["name"].startswith(
        "Test Asset"
    ), f"Created asset name '{test_asset['name']}' does not start with expected prefix"


def test_admin_can_update_asset(
    base_url, test_asset, admin_alpha_token
):  # pylint: disable=redefined-outer-name
    """
    Test that an administrator can successfully update an asset.
    (Checklist item 4)
    """
    asset_id = test_asset["id"]

    # Update the asset
    update_name = generate_timestamped_name("Updated Asset Name")
    update_payload = {
        "name": update_name,
        "region": "us-west-2",
        "tags": {"env": "prod", "updated": "true"},
    }
    with httpx.Client(base_url=base_url) as client:
        update_res = client.put(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
            json=update_payload,
        )
        log_api_response(update_res.request, update_res)

    assert (
        update_res.status_code == 200
    ), f"Admin expected 200 OK for asset update, got {update_res.status_code}"
    updated_data = update_res.json()
    assert (
        updated_data["name"] == update_payload["name"]
    ), "Asset name was not updated correctly"
    assert (
        updated_data["region"] == update_payload["region"]
    ), "Asset region was not updated correctly"

    # Verify the update was persisted with a GET request
    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
    assert (
        get_res.status_code == 200
    ), f"Admin expected 200 OK when verifying updated asset, got {get_res.status_code}"
    assert (
        get_res.json()["name"] == update_payload["name"]
    ), "Updated name was not persisted"


def test_admin_can_delete_asset(
    base_url, admin_alpha_token
):  # pylint: disable=redefined-outer-name
    """
    Test that an administrator can successfully delete an asset.
    (Checklist item 5)
    """
    create_name = generate_timestamped_name("Asset to Delete")
    payload = {
        "name": create_name,
        "asset_type": "EC2",
        "cloud_account": "123",
        "region": "us-east-1",
    }

    with httpx.Client(base_url=base_url) as client:
        create_res = client.post(
            "/assets",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
            json=payload,
        )
    assert create_res.status_code in (
        200,
        201,
    ), f"Failed to create temporary asset: expected 200/201, got {create_res.status_code}"
    asset_id = create_res.json()["id"]

    # Delete the asset
    with httpx.Client(base_url=base_url) as client:
        delete_res = client.delete(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
        log_api_response(delete_res.request, delete_res)

    assert delete_res.status_code in (
        200,
        204,
    ), f"Admin expected 200/204 for asset deletion, got {delete_res.status_code}"

    # Verify deletion
    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
    assert (
        get_res.status_code == 404
    ), f"Asset still exists after deletion: expected 404, got {get_res.status_code}"


def test_user_can_read_asset(
    base_url, test_asset, user_alpha_token
):  # pylint: disable=redefined-outer-name
    """
    Test that a regular user can successfully read an asset.
    (Checklist item 6)
    """
    asset_id = test_asset["id"]

    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(get_res.request, get_res)

    assert (
        get_res.status_code == 200
    ), f"User expected 200 OK for asset read, got {get_res.status_code}"
    assert get_res.json()["id"] == asset_id, "User read returned wrong asset ID"


def test_user_cannot_delete_asset(
    base_url, test_asset, admin_alpha_token, user_alpha_token
):  # pylint: disable=redefined-outer-name
    """
    Test that a regular user cannot delete an asset.
    (Checklist item 7)
    """
    asset_id = test_asset["id"]

    # Try to delete as regular user
    with httpx.Client(base_url=base_url) as client:
        delete_res = client.delete(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
        )
        log_api_response(delete_res.request, delete_res)

    assert (
        delete_res.status_code == 403
    ), "Regular user can delete the asset while shouldn't"

    # Verify asset still exists (as admin)
    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
    assert (
        get_res.status_code == 200
    ), f"Asset missing after failed delete attempt: expected 200 OK, got {get_res.status_code}"


def test_user_cannot_update_asset(
    base_url, test_asset, admin_alpha_token, user_alpha_token
):  # pylint: disable=redefined-outer-name
    """
    Test that a regular user cannot update an asset.
    (Checklist item 8)
    """
    asset_id = test_asset["id"]

    # Try to update as regular user
    update_payload = {"name": "Malicious Update", "region": "us-west-1"}
    with httpx.Client(base_url=base_url) as client:
        update_res = client.put(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {user_alpha_token}"},
            json=update_payload,
        )
        log_api_response(update_res.request, update_res)

    assert (
        update_res.status_code == 403
    ), "Regular user can update the asset while shouldn't"

    # Verify asset remains unchanged (as admin)
    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_alpha_token}"},
        )
    assert (
        get_res.status_code == 200
    ), f"Asset missing after failed update attempt: expected 200 OK, got {get_res.status_code}"
    assert (
        get_res.json()["name"] == test_asset["name"]
    ), "Asset name was modified despite 403 Forbidden"
