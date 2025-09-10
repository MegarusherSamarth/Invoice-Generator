from pydantic import BaseModel
from typing import Optional
 
class Party(BaseModel):
    name: str
    gstin: Optional[str] = None    # None for B2C
    address: str
    state_code: str
    reverse_charge_applicable: bool = False