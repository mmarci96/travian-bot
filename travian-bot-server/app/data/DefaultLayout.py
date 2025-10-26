from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Slot:
    slot_id: str
    building_id: Optional[str] = None
    building_name: Optional[str] = None


@dataclass
class DefaultLayout:
    slots: List[Slot]
