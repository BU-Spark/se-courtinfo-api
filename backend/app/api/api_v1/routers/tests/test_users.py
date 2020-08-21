from uuid import uuid4

from app import models


def test_get_users(client, test_superuser, superuser_token_headers):
    response = client.get("/api/v1/users", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(test_superuser.id),
            "email": test_superuser.email,
            "is_active": test_superuser.is_active,
            "is_superuser": test_superuser.is_superuser,
            "is_county_authorized": test_superuser.is_county_authorized
        }
    ]


def test_delete_user(client, test_superuser, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/users/{test_superuser.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.User).all() == []


def test_delete_user_not_found(client, superuser_token_headers):
    response = client.delete(
        f"/api/v1/users/{uuid4()}", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_user(client, test_superuser, superuser_token_headers):
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": True,
        "is_county_authorized": True,
        "first_name": "Joe",
        "last_name": "Smith",
        "password": "new_password",
    }

    response = client.put(
        f"/api/v1/users/{test_superuser.id}",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_user["id"] = str(test_superuser.id)
    new_user.pop("password")
    assert new_user == response.json()


def test_edit_user_not_found(client, test_db, superuser_token_headers):
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": False,
        "password": "new_password",
    }
    response = client.put(
        f"/api/v1/users/{uuid4()}", json=new_user, headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_user(
        client, test_user, superuser_token_headers,
):
    response = client.get(
        f"/api/v1/users/{test_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_user.id),
        "email": test_user.email,
        "is_active": bool(test_user.is_active),
        "is_superuser": test_user.is_superuser,
        "is_county_authorized": test_user.is_county_authorized
    }


def test_user_not_found(client, superuser_token_headers):
    response = client.get(f"/api/v1/users/{uuid4()}", headers=superuser_token_headers)
    assert response.status_code == 404


def test_authenticated_user_me(client, user_token_headers):
    response = client.get("/api/v1/users/me", headers=user_token_headers)
    assert response.status_code == 200


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    response = client.get("/api/v1/users")
    assert response.status_code == 401
    response = client.get(f"/api/v1/users/{uuid4()}")
    assert response.status_code == 401
    response = client.put(f"/api/v1/users/{uuid4()}")
    assert response.status_code == 401
    response = client.delete(f"/api/v1/users/{uuid4()}")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    response = client.get("/api/v1/users", headers=user_token_headers)
    assert response.status_code == 403
    response = client.get(f"/api/v1/users/{uuid4()}", headers=user_token_headers)
    assert response.status_code == 403


def test_county_authorized_not_allowed(client, county_authorized_token_headers):
    response = client.get("/api/v1/users", headers=county_authorized_token_headers)
    assert response.status_code == 403
    response = client.get(f"/api/v1/users/{uuid4()}", headers=county_authorized_token_headers)
    assert response.status_code == 403
