import csv
from app.models.invoice import Invoice
from app.models.tax_breakdown import TaxBreakdown

def export_csv(invoice: Invoice, breakdown: TaxBreakdown, output_path: str):
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Description", "HSN/SAC", "Qty", "Unit Price", "Taxable",
            "CGST", "SGST", "IGST", "Cess", "Total"
        ])
        for line in breakdown.lines:
            writer.writerow([
                line.description, line.hsn_sac, line.quantity, line.unit_price,
                line.taxable_value, line.cgst, line.sgst, line.igst, line.cess, line.total
            ])
