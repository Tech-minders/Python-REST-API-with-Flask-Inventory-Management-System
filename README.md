# Python-REST-API-with-Flask-Inventory-Management-System

A Flask REST API for managing retail inventory, with OpenFoodFacts integration and a CLI interface.

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/Tech-minders/Python-REST-API-with-Flask-Inventory-Management-System.git
cd inventory-app

# 2. Create a virtual environment
pipenv install
pipenv shell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the Flask server
python app.py

# 5. In a NEW terminal, run the CLI
python cli.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /inventory | Get all items |
| GET | /inventory/\<id\> | Get one item |
| POST | /inventory | Add new item |
| PATCH | /inventory/\<id\> | Update item |
| DELETE | /inventory/\<id\> | Delete item |
| GET | /search/barcode/\<barcode\> | Fetch from OpenFoodFacts by barcode |
| GET | /search/name/\<name\> | Search OpenFoodFacts by name |

## Example POST body

```json
{
  "product_name": "Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Water, almonds",
  "price": 3.99,
  "stock": 50
}
```

## Running Tests

```bash
pytest tests/
```
