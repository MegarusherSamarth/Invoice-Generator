from app.utils.config_loader import load_org_config
from app.rules.hsn_mapper import get_hsn

def build_invoice_from_items(org_id: str, items_input: list):
    config = load_org_config(org_id)
    items = []
    for item in items_input:
        desc = item["description"]
        items.append({
            "description": desc,
            "hsn_sac": get_hsn(desc),
            "quantity": config["defaults"]["quantity"],
            "unit_price": config["defaults"]["unit_price"],
            "tax_rate": config["defaults"]["tax_rate"],
            "is_exempt": False
        })

    return {
        "number": "AUTO-001",
        "date": "2025-09-12",
        "supplier": config["supplier"],
        "customer": config["customer"],
        "place_of_supply_state": config["customer"]["state_code"],
        "items": items
    }
