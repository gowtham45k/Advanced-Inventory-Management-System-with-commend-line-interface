import argparse
from models import Inventory, Product, Invoice
from transactions import TransactionManager
from invoice_generator import InvoiceGenerator
from inventory_manager import save_inventory, load_inventory

INVENTORY_FILE = 'inventory.json'

def main():
    parser = argparse.ArgumentParser(description="Advanced Inventory Management System CLI")
    parser.add_argument('command', choices=['add', 'update', 'remove', 'sale', 'return', 'invoice'], help='Command to execute')
    parser.add_argument('--product_id', help='Product ID')
    parser.add_argument('--name', help='Product Name')
    parser.add_argument('--price', type=float, help='Product Price')
    parser.add_argument('--category', help='Product Category')
    parser.add_argument('--quantity', type=int, help='Product Quantity')
    parser.add_argument('--reason', help='Return Reason')
    args = parser.parse_args()

    inventory = load_inventory(INVENTORY_FILE)
    transaction_manager = TransactionManager(inventory)
    invoice_generator = InvoiceGenerator('invoices')

    if args.command == 'add':
        product = Product(args.product_id, args.name, args.price, args.category, args.quantity)
        inventory.add_product(product)
        save_inventory(inventory, INVENTORY_FILE)
        print(f"Added product: {product}")

    elif args.command == 'update':
        inventory.update_product(args.product_id, args.quantity, args.price)
        save_inventory(inventory, INVENTORY_FILE)
        print(f"Updated product {args.product_id}")

    elif args.command == 'remove':
        inventory.remove_product(args.product_id)
        save_inventory(inventory, INVENTORY_FILE)
        print(f"Removed product {args.product_id}")

    elif args.command == 'sale':
        transaction_manager.record_sale(args.product_id, args.quantity, args.price)
        save_inventory(inventory, INVENTORY_FILE)
        print(f"Recorded sale for product {args.product_id}")

    elif args.command == 'return':
        transaction_manager.record_return(args.product_id, args.quantity, args.reason)
        save_inventory(inventory, INVENTORY_FILE)
        print(f"Recorded return for product {args.product_id}")

    elif args.command == 'invoice':
        sales = [sale for sale in transaction_manager.sales if sale.product_id == args.product_id]
        if sales:
            invoice = Invoice(f"INV-{len(sales) + 1}", sales)
            invoice_file = invoice_generator.generate_invoice(invoice)
            print(f"Generated invoice: {invoice_file}")
        else:
            print(f"No transactions found for product ID {args.product_id}")

if __name__ == '__main__':
    main()
