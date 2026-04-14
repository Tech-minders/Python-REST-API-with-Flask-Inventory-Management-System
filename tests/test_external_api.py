import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from external_api import fetch_product_by_barcode, search_product_by_name, format_api_product


def test_fetch_product_by_barcode_found():
    fake_response = {
        "status": 1,
        "product": {
            "product_name": "Fake Milk",
            "brands": "Fake Brand",
            "ingredients_text": "Water, milk"
        }
    }
    with patch("external_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response
        result = fetch_product_by_barcode("1234567890")
        assert result is not None
        assert result["product_name"] == "Fake Milk"


def test_fetch_product_by_barcode_not_found():
    with patch("external_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": 0}
        assert fetch_product_by_barcode("0000000000") is None


def test_fetch_product_by_barcode_network_error():
    import requests as req
    with patch("external_api.requests.get") as mock_get:
        mock_get.side_effect = req.exceptions.ConnectionError("No internet")
        assert fetch_product_by_barcode("1234567890") is None


def test_search_product_by_name_found():
    fake_response = {
        "products": [
            {"product_name": "Almond Milk A", "brands": "Brand A"},
            {"product_name": "Almond Milk B", "brands": "Brand B"},
            {"product_name": "Almond Milk C", "brands": "Brand C"},
        ]
    }
    with patch("external_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response
        result = search_product_by_name("almond milk")
        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0]["product_name"] == "Almond Milk A"


def test_search_product_by_name_empty():
    with patch("external_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"products": []}
        assert search_product_by_name("xyznonexistentproduct") == []


def test_search_product_by_name_network_error():
    import requests as req
    with patch("external_api.requests.get") as mock_get:
        mock_get.side_effect = req.exceptions.ConnectionError("No internet")
        assert search_product_by_name("milk") == []


def test_format_api_product():
    raw_product = {
        "product_name": "Organic Juice",
        "brands": "Good Brand",
        "ingredients_text": "Orange juice",
        "nutrition_grades": "a",
        "allergens": "None",
        "categories": "Beverages",
        "nutriments": {
            "energy-kcal_100g": 45,
            "fat_100g": 0.1,
            "sugars_100g": 10.2,
            "proteins_100g": 0.7
        },
        "unwanted_field": "ignored"
    }
    result = format_api_product(raw_product)

    assert result["product_name"] == "Organic Juice"
    assert result["brands"] == "Good Brand"
    assert result["ingredients_text"] == "Orange juice"
    assert result["nutriscore_grade"] == "A"
    assert result["allergens"] == "None"
    assert result["categories"] == "Beverages"
    assert result["energy_kcal_100g"] == 45
    assert result["fat_100g"] == 0.1
    assert result["sugars_100g"] == 10.2
    assert result["proteins_100g"] == 0.7
    assert result["price"] == 0.00
    assert result["stock"] == 0
    assert "unwanted_field" not in result


def test_format_api_product_missing_fields():
    result = format_api_product({})
    assert result["product_name"] == "Unknown"
    assert result["brands"] == "Unknown"
    assert result["ingredients_text"] == "Not available"
    assert result["nutriscore_grade"] == "UNKNOWN"
    assert result["energy_kcal_100g"] is None