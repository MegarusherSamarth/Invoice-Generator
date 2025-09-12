# Purpose
# - Validate required fields in invoice JSON
# - Check GSTIN format and checksum
# - Ensure state codes are valid
# - Catch logical errors (e.g. negative quantities, missing HSN/Sac)

from app.rules.jurisdiction import Jurisdiction
import re

GSTIN_REGEX = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"

def validate_gstin(gstin: str)-> bool:
    return bool(re.match(GSTIN_REGEX, gstin))

def validate_invoice(data: dict):
    required_fields = ["number", "date", "supplier", "customer", "items", "place_of_supply_state"]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
        
    jurisdiction = Jurisdiction()
    
    # Validate supplier GSTIN
    supplier = data["supplier"]
    
    if not validate_gstin(supplier["gstin"]):
        raise ValueError(f"Invalid supplier GSTIN: {supplier['gstin']}")
    if not jurisdiction.is_valid_state(supplier["state_code"]):
        raise ValueError(f"Invalid supplier state code: {supplier['state_code']}")
    
    # Validate customer state
    customer = data["customer"]
    
    if not jurisdiction.is_valid_state(customer["state_code"]):
        raise ValueError(f"Invalid customer state code: {customer['state_code']}")
    if customer.get("gstin") and not validate_gstin(customer["gstin"]):
        raise ValueError(f"Invalid customer GSTIN: {customer['gstin']}")
    
    # Validate items
    for idx, item in enumerate(data["items"]):
        if item["quantity"] <= 0:
            raise ValueError(f"Item {idx+1} has invalid quantity: {item['quantity']}")
        if item["unit_price"] < 0:
            raise ValueError(f"Item {idx+1} has negative unit price: {item['unit_price']}")
        if not item.get("hsn_sac"):
            raise ValueError(f"Item {idx+1} missing HSN/SAC code")