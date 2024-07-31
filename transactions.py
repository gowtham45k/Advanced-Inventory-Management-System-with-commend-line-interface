from models import Sale, Returns
from datetime import datetime
import uuid

class TransactionManager:
    def __init__(self, inventory):
        self.inventory = inventory
        self.sales = []
        self.returns = []

    def record_sale(self, product_id: str, quantity: int, price: float):
        """Record a sale transaction and update the inventory."""
        if product_id not in self.inventory.products:
            raise ValueError("Product ID not found")
        
        product = self.inventory.products[product_id]
        if product.quantity < quantity:
            raise ValueError("Not enough inventory")

        transaction_id = str(uuid.uuid4())
        sale = Sale(transaction_id, product_id, quantity, price, datetime.now())
        self.sales.append(sale)
        product.quantity -= quantity

    def record_return(self, product_id: str, quantity: int, reason: str):
        """Record a return transaction and update the inventory."""
        if product_id not in self.inventory.products:
            raise ValueError("Product ID not found")

        product = self.inventory.products[product_id]
        transaction_id = str(uuid.uuid4())
        return_transaction = Returns(transaction_id, product_id, quantity, reason, datetime.now())
        self.returns.append(return_transaction)
        product.quantity += quantity
