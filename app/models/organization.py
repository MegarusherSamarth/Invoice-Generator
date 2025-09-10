from pydantic import BaseModel, Field
from typing import Optional

class Organization(BaseModel):
    gstin: str = Field(..., description="GSTIN of the supplier")
    legal_name: str
    trade_name: Optional[str]= None
    address: str
    state_code: str = Field(..., min_length=2, max_length=2)
    composition: bool = False
    e_invoice_enabled: bool = False
    logo_url: Optional[str] = None