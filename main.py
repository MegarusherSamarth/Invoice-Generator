import json
from app.services.invoice_processor import process_invoice

with open("data/sample_invoice.json") as f:
    invoice_data = json.load(f)

outputs = process_invoice(invoice_data)
print("Generated files:", outputs)
