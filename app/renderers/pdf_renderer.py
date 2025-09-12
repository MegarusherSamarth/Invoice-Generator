# Purpose
# - USe Jinja2 to render invoice data into HTML
# - Convert HTML to PDF using WeasyPrint
# - Embed tax breakdown, HSN/Sac, CGST/SGST/IGST, and optional declarations

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.models.invoice import Invoice
from app.models.tax_breakdown import TaxBreakdown
from pathlib import Path

env = Environment(loader=FileSystemLoader("templates"))

def render_invoice_html(invoice: Invoice, breakdown: TaxBreakdown) -> str:
    template = env.get_template("invoice.html")
    return template.render(invoice=invoice, breakdown=breakdown)

def generate_pdf(invoice: Invoice, breakdown: TaxBreakdown, output_path: str):
    html_content = render_invoice_html(invoice, breakdown)
    HTML(string=html_content).write_pdf(output_path)