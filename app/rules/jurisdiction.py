# Purpose
# - Load state codes and metadata from config/states.yaml
# - Determine supply type based on supplier and place-of-supply states
# - Validate state codes and handle union territories if needed

import yaml
from pathlib import Path

class Jurisdiction:
    def __init__(self, config_path: str = "config/states.yaml"):
        self.states = {}
        self._load_states(config_path)
    
    def _load_states(self, path: str):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            self.states = data.get("states", {})
        
    def is_valid_state(self, code: str)-> bool:
        return code in self.states
    
    def get_state_name(self, code: str)-> str:
        return self.states.get(code, {}).get("name", "Unknown")
    
    def is_union_territory(self, code: str)-> bool:
        return self.states.get(code, {}).get("is_ut", False)
    
    def is_inter_state_supply(self, supplier_state: str, pos_state: str)-> bool:
        if not self.is_valid_state(supplier_state) or not self.is_valid_state(pos_state):
            raise ValueError(f"Invalid state codes: {supplier_state}, {pos_state}")
        return supplier_state != pos_state