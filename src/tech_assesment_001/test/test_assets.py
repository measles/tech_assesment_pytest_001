"""Tests for asset management."""

import httpx
import pytest

from tech_assesment_001.utils.credentials import load_credentials
from tech_assesment_001.utils.data import generate_timestamped_name
from tech_assesment_001.utils.logger import log_api_response


@pytest.fixture
def created_assets(base_url, auth_tokens):  # pylint: disable=redefined-outer-name
    """
    Fixture to track created assets and delete them after the test.
    """
    assets_to_delete = []
    yield assets_to_delete

    if not assets_to_delete:
        return

    # Teardown: delete all created assets
    orgs = load_credentials()
    org_alpha = orgs["org-alpha"]
    admin_creds = org_alpha.admin
    if not admin_creds:
        return

    admin_token = auth_tokens(admin_creds.email, admin_creds.password)
    with httpx.Client(base_url=base_url) as client:
        for asset_id in assets_to_delete:
            response = client.delete(
                f"/assets/{asset_id}",
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            log_api_response(response.request, response)


def test_user_regardless_of_role_can_read_assets(
    base_url, auth_tokens
):  # pylint: disable=redefined-outer-name
    """
    Test that both admin and regular users can read the asset list.
    (Checklist item 2)
    """
    orgs = load_credentials()
    assert "org-alpha" in orgs
    org_alpha = orgs["org-alpha"]

    # 1. Test as Admin
    admin_creds = org_alpha.admin
    assert admin_creds, "Admin credentials for org-alpha not found"
    admin_token = auth_tokens(admin_creds.email, admin_creds.password)

    with httpx.Client(base_url=base_url) as client:
        admin_response = client.get(
            "/assets",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        log_api_response(admin_response.request, admin_response)
    assert admin_response.status_code == 200

    # 2. Test as Regular User
    user_creds = org_alpha.user
    assert user_creds, "User credentials for org-alpha not found"
    user_token = auth_tokens(user_creds.email, user_creds.password)

    with httpx.Client(base_url=base_url) as client:
        user_response = client.get(
            "/assets",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        log_api_response(user_response.request, user_response)
    assert user_response.status_code == 200

    # Basic validation of response structure
    admin_data = admin_response.json()
    user_data = user_response.json()

    assert "items" in admin_data
    assert isinstance(admin_data["items"], list)
    assert "items" in user_data
    assert isinstance(user_data["items"], list)


def test_admin_can_create_asset(
    base_url, created_assets, auth_tokens
):  # pylint: disable=redefined-outer-name
    """
    Test that an administrator can successfully create an asset.
    (Checklist item 3)
    """
    orgs = load_credentials()
    org_alpha = orgs["org-alpha"]
    admin_creds = org_alpha.admin
    assert admin_creds, "Admin credentials for org-alpha not found"
    admin_token = auth_tokens(admin_creds.email, admin_creds.password)

    asset_name = generate_timestamped_name("Test Asset Admin")
    asset_payload = {
        "name": asset_name,
        "asset_type": "EC2",
        "cloud_account": "123456789",
        "region": "us-east-1",
        "tags": {"environment": "test", "created_by": "pytest"},
    }

    with httpx.Client(base_url=base_url) as client:
        response = client.post(
            "/assets",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=asset_payload,
        )
        log_api_response(response.request, response)

    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data
    created_assets.append(data["id"])

    assert data["name"] == asset_payload["name"]
    assert data["asset_type"] == asset_payload["asset_type"]


def test_admin_can_update_asset(
    base_url, created_assets, auth_tokens
):  # pylint: disable=redefined-outer-name,too-many-locals
    """
    Test that an administrator can successfully update an asset.
    (Checklist item 4)
    """
    orgs = load_credentials()
    org_alpha = orgs["org-alpha"]
    admin_creds = org_alpha.admin
    assert admin_creds, "Admin credentials for org-alpha not found"
    admin_token = auth_tokens(admin_creds.email, admin_creds.password)

    # 1. Create an asset to update
    create_name = generate_timestamped_name("Asset to Update")
    create_payload = {
        "name": create_name,
        "asset_type": "EC2",
        "cloud_account": "123456789",
        "region": "us-east-1",
        "tags": {"env": "dev"},
    }
    with httpx.Client(base_url=base_url) as client:
        create_res = client.post(
            "/assets",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=create_payload,
        )
        log_api_response(create_res.request, create_res)

    assert create_res.status_code in (200, 201)
    asset_id = create_res.json()["id"]
    created_assets.append(asset_id)

    # 2. Update the asset
    update_name = generate_timestamped_name("Updated Asset Name")
    update_payload = {
        "name": update_name,
        "region": "us-west-2",
        "tags": {"env": "prod", "updated": "true"},
    }
    with httpx.Client(base_url=base_url) as client:
        update_res = client.put(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=update_payload,
        )
        log_api_response(update_res.request, update_res)

    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["name"] == update_payload["name"]
    assert updated_data["region"] == update_payload["region"]
    assert updated_data["tags"]["env"] == "prod"

    # 3. Verify the update was persisted with a GET request
    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        log_api_response(get_res.request, get_res)

    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["name"] == update_payload["name"]
    assert get_data["region"] == update_payload["region"]
    assert get_data["tags"]["env"] == "prod"


def test_admin_can_delete_asset(
    base_url, created_assets, auth_tokens
):  # pylint: disable=redefined-outer-name
    """
    Test that an administrator can successfully delete an asset.
    (Checklist item 5)
    """
    orgs = load_credentials()
    org_alpha = orgs["org-alpha"]
    admin_creds = org_alpha.admin
    assert admin_creds, "Admin credentials for org-alpha not found"
    admin_token = auth_tokens(admin_creds.email, admin_creds.password)

    # 1. Create an asset to delete
    create_name = generate_timestamped_name("Asset to Delete")
    create_payload = {
        "name": create_name,
        "asset_type": "EC2",
        "cloud_account": "123456789",
        "region": "us-east-1",
    }
    with httpx.Client(base_url=base_url) as client:
        create_res = client.post(
            "/assets",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=create_payload,
        )
        log_api_response(create_res.request, create_res)

    assert create_res.status_code in (200, 201)
    asset_id = create_res.json()["id"]
    created_assets.append(asset_id)

    # 2. Delete the asset
    with httpx.Client(base_url=base_url) as client:
        delete_res = client.delete(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        log_api_response(delete_res.request, delete_res)

    assert delete_res.status_code in (200, 204)

    # 3. Verify deletion with a GET request
    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        log_api_response(get_res.request, get_res)

    assert get_res.status_code == 404


def test_user_can_read_asset(
    base_url, created_assets, auth_tokens
):  # pylint: disable=redefined-outer-name,too-many-locals
    """
    Test that a regular user can successfully read an asset.
    (Checklist item 6)
    """
    orgs = load_credentials()
    org_alpha = orgs["org-alpha"]
    admin_creds = org_alpha.admin
    user_creds = org_alpha.user
    assert admin_creds and user_creds, "Credentials for org-alpha not found"

    admin_token = auth_tokens(admin_creds.email, admin_creds.password)
    user_token = auth_tokens(user_creds.email, user_creds.password)

    # 1. Create an asset as admin
    create_name = generate_timestamped_name("User Read Asset")
    create_payload = {
        "name": create_name,
        "asset_type": "EC2",
        "cloud_account": "123456789",
        "region": "us-east-1",
    }
    with httpx.Client(base_url=base_url) as client:
        create_res = client.post(
            "/assets",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=create_payload,
        )
        log_api_response(create_res.request, create_res)

    assert create_res.status_code in (200, 201)
    asset_id = create_res.json()["id"]
    created_assets.append(asset_id)

    # 2. Read the asset as regular user
    with httpx.Client(base_url=base_url) as client:
        get_res = client.get(
            f"/assets/{asset_id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        log_api_response(get_res.request, get_res)

    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["id"] == asset_id
    assert get_data["name"] == create_name
