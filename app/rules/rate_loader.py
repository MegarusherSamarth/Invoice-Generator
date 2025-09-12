# Purpose
# - Load GST rates from gst_rates.yaml
# - Provide lookup by HSN/SAC code
# Fallback to default rate if code not found

import yaml
from decimal import Decimal
from pathlib import Path

class RateLoader:
    def __init__(self, config_path: str = "config/gst_rates.yaml"):
        self.rates = {}
        self.defaults = {"rate": Decimal("18"), "cess": Decimal("0")}
        self._load_rates(config_path)
    
    def _load_rates(self, path: str):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            self.rates = {
                str(code): {
                    "rate": Decimal(str(info.get("rate", self.defaults["rate"]))),
                    "cess": Decimal(str(info.get("cess", self.defaults["cess"]))),
                }
                for code, info in data.get("rates", {}).items()
            }
            self.defaults = {
                "rate": Decimal(str(data.get("defualts", {}).get("rate", 18))),
                "cess": Decimal(str(data.get("defualts", {}).get("cess", 0)))
            }
    
    def get_rate(self, hsn_sac: str)-> dict:
        # Exact Match
        if hsn_sac in self.rates:
            return self.rates[hsn_sac]
        # Wildcard prefix match (e.g. "27*" matches "2710")
        for code in self.rates:
            if code.endswith("*") and hsn_sac.startswith(code[:-1]):
                return self.rates[code]
        
        # Fallback to default
        return self.defaults