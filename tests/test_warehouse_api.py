import os

import pytest
from fastapi.testclient import TestClient

from db.base import database
from main import app


@pytest.fixture(scope="module")
def temp_db():
    testing = False
    if os.environ['TESTING'] == 'True':
        testing = True
    elif os.environ['TESTING'] == 'False':
        testing = False
    if not testing:
        pytest.skip(".env TESTING set True")
    try:
        yield database
    finally:
        if os.path.isfile(os.environ['DATABASE_URL_TESTING_PATCH']):
            os.remove(os.environ['DATABASE_URL_TESTING_PATCH'])


client = TestClient(app)

SELLER = {
    "login": "seller",
    "type": "sellers",
    "password": "seller",
    "password2": "seller"
}
SELLER_LOGIN = {
    "login": "seller",
    "password": "seller",
}
BUYER = {
    "login": "buyer",
    "type": "buyers",
    "password": "buyer",
    "password2": "buyer"
}
BUYER_LOGIN = {
    "login": "buyer",
    "password": "buyer",
}


def test_main(temp_db):
    response = client.get("/")
    assert response.status_code == 200


def test_users_register_seller(temp_db):
    response = client.post("/users/register", json=SELLER)
    assert response.status_code == 200
    assert response.json()["login"] == "seller"
    assert response.json()["type"] == "sellers"


def test_users_register_buyer(temp_db):
    response = client.post("/users/register", json=BUYER)
    assert response.status_code == 200
    assert response.json()["login"] == "buyer"
    assert response.json()["type"] == "buyers"


def test_users_read(temp_db):
    response = client.get("/users/read?limit=100&skip=0")
    assert response.status_code == 200


def test_user_update(temp_db):
    response = client.post("/auth/", json=BUYER_LOGIN)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post("/auth/", json=BUYER_LOGIN, headers=headers)
    buyer2 = {
        "login": "buyer2",
        "type": "buyers",
        "password": "buyer2",
        "password2": "buyer2"
    }
    response = client.put("/users/update", json=buyer2, params={'id': 2}, headers=headers)
    assert response.status_code == 200
    assert response.json()["login"] == "buyer2"


def test_auth(temp_db):
    response = client.post("/auth/", json=SELLER_LOGIN)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post("/auth/", json=SELLER_LOGIN, headers=headers)


def test_warehouses(temp_db):
    response = client.post("/auth/", json=SELLER_LOGIN)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get("/warehouses/", json=SELLER_LOGIN, headers=headers)


def test_warehouses_add(temp_db):
    response = client.post("/auth/", json=SELLER_LOGIN)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    product = {
        "product": "apple",
        "amount": 10
    }
    response = client.post("/warehouses/add", json=product, headers=headers)
    assert response.status_code == 200


def test_warehouses_add_forbidden(temp_db):
    response = client.post("/auth/", json={"login": "buyer2", "password": "buyer2"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    product = {
        "product": "apple",
        "amount": 10
    }
    response = client.post("/warehouses/add", json=product, headers=headers)
    assert response.status_code == 403


def test_warehouses_put(temp_db):
    response = client.post("/auth/", json=SELLER_LOGIN)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    product = {
        "product": "apple",
        "amount": 10
    }
    response = client.put("/warehouses/put", json=product, headers=headers)
    assert response.status_code == 200


def test_warehouses_put_forbidden(temp_db):
    response = client.post("/auth/", json={"login": "buyer2", "password": "buyer2"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    product = {
        "product": "apple",
        "amount": 10
    }
    response = client.put("/warehouses/put", json=product, headers=headers)
    assert response.status_code == 403


def test_warehouses_buy(temp_db):
    response = client.post("/auth/", json={"login": "buyer2", "password": "buyer2"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    product = {
        "product": "apple",
        "amount": 10
    }
    response = client.put("/warehouses/buy", json=product, headers=headers)
    assert response.status_code == 200


def test_warehouses_buy_forbidden(temp_db):
    response = client.post("/auth/", json=SELLER_LOGIN)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {access_token}'}
    product = {
        "product": "apple",
        "amount": 10
    }
    response = client.put("/warehouses/buy", json=product, headers=headers)
    assert response.status_code == 403
