
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "price": 3.99,
        "stock": 50
    },
    {
        "id": 2,
        "product_name": "Whole Grain Oats",
        "brands": "Quaker",
        "ingredients_text": "Whole grain rolled oats",
        "price": 2.49,
        "stock": 120
    },
    {
        "id": 3,
        "product_name": "Greek Yogurt",
        "brands": "Chobani",
        "ingredients_text": "Cultured nonfat milk, live active cultures",
        "price": 1.99,
        "stock": 75
    },
    {
        "id": 4,
        "product_name": "Honey",
        "brands": "Nature Nate's",
        "ingredients_text": "100% pure raw unfiltered honey",
        "price": 8.99,
        "stock": 30
    },
    {
        "id": 5,
        "product_name": "Olive Oil",
        "brands": "Kirkland",
        "ingredients_text": "Extra virgin olive oil",
        "price": 12.99,
        "stock": 40
    }
]

#Generate a new unique ID
def get_next_id():
    if len(inventory) == 0:
        return 1  # if list is empty, start from 1
    biggest_id = max(item["id"] for item in inventory)
    return biggest_id + 1


# Find one item by its ID

def find_item_by_id(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None  