import json
from app.models.invoice import Invoice
from app.models.tax_breakdown import TaxBreakdown

def export_json(invoice: Invoice, breakdown: TaxBreakdown, output_path: str):
    data = {
        "invoice": invoice.model_dump(),
        "tax_breakdown": breakdown.model_dump()
    }
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
