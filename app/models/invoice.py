from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from decimal import Decimal
from .organization import Organization
from .party import Party
from .item import Item

class Invoice(BaseModel):
    number: str
    date: str    # ISO format: YYYY-MM-DD
    supplier: Organization
    customer: Party
    place_of_supply_state: str
    items: List[Item]
    freight: Decimal = Decimal("0")
    insurance: Decimal = Decimal("0")
    other_charges: Decimal = Decimal("0")
    notes: Optional[str] = None
    rounding: Literal["nearest", "up", "down"] = "nearest"
    po_reference: Optional[str] = None
    payment_terms: Optional[str] = None