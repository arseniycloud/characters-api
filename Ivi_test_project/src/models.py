from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Character:
    name: str
    universe: Optional[str] = None
    education: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    identity: Optional[str] = None

    def to_dict(self):
        pass
