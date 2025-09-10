from pydantic import BaseModel, Field
from decimal import Decimal

class Item(BaseModel):
    description: str
    hsn_sac: str
    quantity: Decimal = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    tax_rate: Decimal = Field(..., gt=0)   # e.g., 18 for 18%
    cess_rate: Decimal = Field(default=Decimal("0"), ge=0)
    discount_pre_tax: Decimal = Field(default=Decimal("0"), ge=0)
    discount_post_tax: Decimal = Field(default=Decimal("0"), ge=0)
    is_exempt: bool = False
    