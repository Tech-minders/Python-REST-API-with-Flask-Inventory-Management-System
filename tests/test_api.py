import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_one_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_item_not_found(client):
    response = client.get("/inventory/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_add_item(client):
    new_item = {
        "product_name": "Test Product",
        "brands": "Test Brand",
        "price": 5.99,
        "stock": 10
    }
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Product"
    assert "id" in data


def test_add_item_missing_fields(client):
    response = client.post("/inventory", json={"product_name": "No Price Item"})
    assert response.status_code == 400


def test_update_item(client):
    response = client.patch("/inventory/1", json={"price": 99.99})
    assert response.status_code == 200
    assert response.get_json()["price"] == 99.99


def test_delete_item(client):
    post_response = client.post("/inventory", json={"product_name": "Delete Me", "price": 1.00, "stock": 1})
    created_id = post_response.get_json()["id"]

    assert client.delete(f"/inventory/{created_id}").status_code == 200
    assert client.get(f"/inventory/{created_id}").status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/9999")
    assert response.status_code == 404