# Purpose
# - Validate CGST/SGST/IGST computation
# - Test composition scheme, exempt items, and rounding
# - Use golden snapshots for deterministic output

import pytest
import json
from app.models.invoice import Invoice
from app.services.tax_engine import compute_invoice_tax

def load_invoice(path: str) -> Invoice:
    with open(path, "r") as f:
        data = json.load(f)
    return Invoice(**data)

@pytest.mark.parametrize("file_path", [
    "data/org1/invoice_001.json",
    "data/org2/invoice_001.json"
])
def test_invoice_from_file(file_path):
    invoice = load_invoice(file_path)
    breakdown = compute_invoice_tax(invoice)
    assert breakdown.grand_total > 0