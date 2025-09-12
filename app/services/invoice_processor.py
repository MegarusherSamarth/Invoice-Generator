# Purpose
# - Load invoice data (from JSON or object)
# - Validate structure and GSTINs
# - Compute tax breakdown
# - Render output (PDF, JSON, CSV)
# - Log and handle errors gracefully

from app.models.invoice import Invoice
from app.services.tax_engine import compute_invoice_tax
from app.renderers.pdf_renderer import generate_pdf
from app.renderers.json_exporter import export_json
from app.renderers.csv_exporter import export_csv
from app.validators.invoice_validator import validate_invoice
from app.utils.logger import log_info, log_error

def process_invoice(invoice_data: dict, output_dir: str = "output"):
    try:
        # Step 1: Validate Input
        validate_invoice(invoice_data)
        
        # Step 2: Parse into Model
        invoice = Invoice(**invoice_data)
        
        # Step 3: Compute Tax
        breakdown = compute_invoice_tax(invoice)
        
        # Step 4: Render Outputs
        pdf_path = f"{output_dir}/{invoice.number}.pdf"
        json_path = f"{output_dir}/{invoice.number}.json"
        csv_path = f"{output_dir}/{invoice.number}.csv"
        
        generate_pdf(invoice, breakdown, pdf_path)
        export_json(invoice, breakdown, json_path)
        export_csv(invoice, breakdown, csv_path)
        
        log_info(f"Invoice {invoice.number} processed successfully.")
        return {
            "pdf": pdf_path, "json": json_path, "csv": csv_path
        }
    
    except Exception as e:
        log_error(f"Failed to process invoice: {e}")
        raise