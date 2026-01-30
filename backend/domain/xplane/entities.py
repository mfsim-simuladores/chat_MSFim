from dataclasses import dataclass
from typing import Optional


@dataclass
class AircraftStatus:
    raw: dict

    def get_float(self, key: str) -> Optional[float]:
        v = self.raw.get(key)
        try:
            return float(v.replace(",", ".")) if v is not None else None
        except:
            return None

    def get_int(self, key: str) -> Optional[int]:
        v = self.raw.get(key)
        try:
            return int(v)
        except:
            return None

    def get_bool(self, key: str) -> bool:
        return self.raw.get(key) == "1"
