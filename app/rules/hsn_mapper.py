HSN_MAP = {
    "Software License": "997331",
    "Cloud Hosting": "998315",
    "Consulting": "998312"
}

def get_hsn(description: str) -> str:
    return HSN_MAP.get(description, "999999")  # fallback
