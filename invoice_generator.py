from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from typing import List
from models import Invoice, Sale
import os

class InvoiceGenerator:
    def __init__(self, invoices_dir: str):
        self.invoices_dir = invoices_dir
        os.makedirs(invoices_dir, exist_ok=True)

    def generate_invoice(self, invoice: Invoice):
        """Generate a PDF invoice for the given invoice."""
        file_path = os.path.join(self.invoices_dir, f"{invoice.invoice_id}.pdf")
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.drawString(1 * inch, height - 1 * inch, f"Invoice ID: {invoice.invoice_id}")
        c.drawString(1 * inch, height - 1.5 * inch, f"Date: {invoice.transactions[0].date.strftime('%Y-%m-%d %H:%M:%S')}")

        y = height - 2 * inch
        for transaction in invoice.transactions:
            c.drawString(1 * inch, y, f"Product ID: {transaction.product_id}")
            c.drawString(3 * inch, y, f"Quantity: {transaction.quantity}")
            c.drawString(4 * inch, y, f"Price: ${transaction.price:.2f}")
            y -= 0.5 * inch

        c.drawString(1 * inch, y, f"Total Amount: ${invoice.total_amount:.2f}")
        c.save()
        return file_path

    def list_invoices_for_product(self, product_id: str) -> List[str]:
        """List all invoice files for a specific product."""
        invoices = []
        for file_name in os.listdir(self.invoices_dir):
            if file_name.endswith(".pdf"):
                with open(os.path.join(self.invoices_dir, file_name), 'r') as file:
                    if product_id in file.read():
                        invoices.append(file_name)
        return invoices
