# Connects to the OpenFoodFacts API (https://world.openfoodfacts.net)

import requests

BASE_URL = "https://world.openfoodfacts.net"

HEADERS = {
    "User-Agent": "InventoryApp/1.0 (inventory@example.com)"
}


# Fetch product by barcode 
def fetch_product_by_barcode(barcode):
    try:
        url = f"{BASE_URL}/api/v2/product/{barcode}.json"
        response = requests.get(url, headers=HEADERS, timeout=5)

        data = response.json()

        if data.get("status") == 1:  # status 1 = product found
            return data["product"]
        else:
            return None

    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")
        return None


# Search product by name 
def search_product_by_name(product_name):
    try:
        formatted_name = product_name.replace(" ", "+")
        url = (
            f"https://world.openfoodfacts.org/cgi/search.pl"
            f"?search_terms={formatted_name}&search_simple=1&action=process&json=1"
        )

        response = requests.get(url, headers=HEADERS, timeout=5)
        data = response.json()

        products = data.get("products", [])
        return products[:5]  # return at most 5 results

    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")
        return []


# Format raw API product into enriched inventory format

def format_api_product(api_product):
    nutriments = api_product.get("nutriments", {})

    return {
        "product_name": api_product.get("product_name", "Unknown"),
        "brands": api_product.get("brands", "Unknown"),
        "ingredients_text": api_product.get("ingredients_text", "Not available"),
        "nutriscore_grade": api_product.get("nutrition_grades", "Unknown").upper(),
        "allergens": api_product.get("allergens", "None listed"),
        "categories": api_product.get("categories", "Unknown"),
        "energy_kcal_100g": nutriments.get("energy-kcal_100g", None),
        "fat_100g": nutriments.get("fat_100g", None),
        "sugars_100g": nutriments.get("sugars_100g", None),
        "proteins_100g": nutriments.get("proteins_100g", None),
        "price": 0.00,  
        "stock": 0    
    }