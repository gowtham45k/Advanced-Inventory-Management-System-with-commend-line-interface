import json
from models import Inventory, Product

def save_inventory(inventory: Inventory, filename: str):
    """Save the current state of the inventory to a file."""
    with open(filename, 'w') as file:
        data = {product_id: vars(product) for product_id, product in inventory.products.items()}
        json.dump(data, file)

def load_inventory(filename: str) -> Inventory:
    """Load inventory state from a file."""
    inventory = Inventory()
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            for product_id, product_data in data.items():
                product = Product(
                    product_id=product_data['product_id'],
                    name=product_data['name'],
                    price=product_data['price'],
                    category=product_data['category'],
                    quantity=product_data['quantity']
                )
                inventory.add_product(product)
    except FileNotFoundError:
        pass  # If no file exists, start with an empty inventory
    return inventory
