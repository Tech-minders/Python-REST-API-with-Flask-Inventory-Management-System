# It defines all the API routes that clients can call

from flask import Flask, request, jsonify  
from database import inventory, find_item_by_id, get_next_id 

app = Flask(__name__) 


# GET /inventory -> Fetch all items
@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200 

# GET /inventory/<id> -> Fetch a single item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_one_item(item_id):
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404 

    return jsonify(item), 200


# POST /inventory -> Add a new item

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()  

    required_fields = ["product_name", "price", "stock"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400  

    new_item = {
        "id": get_next_id(),
        "product_name": data["product_name"],
        "brands": data.get("brands", "Unknown"),          
        "ingredients_text": data.get("ingredients_text", ""),  
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item) 

    return jsonify(new_item), 201  # Created


# PATCH /inventory/<id> -> Update an item

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    data = request.get_json()

    # Update only the fields that were sent and leave the rest unchanged
    updatable_fields = ["product_name", "brands", "ingredients_text", "price", "stock"]
    for field in updatable_fields:
        if field in data:
            item[field] = data[field]  # overwrite 

    return jsonify(item), 200

# DELETE /inventory/<id> -> Remove an item

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    inventory.remove(item)

    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)