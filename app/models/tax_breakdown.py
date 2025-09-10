from pydantic import BaseModel
from decimal import Decimal
from typing import List, Dict

class TaxLine(BaseModel):
    description: str
    hsn_sac: str
    quantity: Decimal
    unit_price: Decimal
    taxable_value: Decimal
    cgst: Decimal
    sgst: Decimal
    igst: Decimal
    cess: Decimal
    total: Decimal
    
class TaxBreakdown(BaseModel):
    lines: List[TaxLine]
    total_taxable: Decimal
    cgst_total: Decimal
    sgst_total: Decimal
    igst_total: Decimal
    cess_total: Decimal
    subtotal: Decimal
    rounding_adjustment: Decimal
    grand_total: Decimal