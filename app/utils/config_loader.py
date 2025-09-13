import yaml

def load_org_config(org_id: str) -> dict:
    with open(f"config/{org_id}/defaults.yaml", "r") as f:
        return yaml.safe_load(f)
