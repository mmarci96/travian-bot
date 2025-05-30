from dataclasses import dataclass
from typing import List


class Slot:
    """docstring for Slot."""

    def __init__(self, slot_id: str, building_id: str, building_name):
        super(Slot, self).__init__()
        self.slot_id = slot_id
        self.building_id = building_id
        self.building_name = building_name


@dataclass
class DefaultLayout:
    """docstring for DefaultLayout."""

    def __init__(self, slots: List[Slot]):
        super(DefaultLayout, self).__init__()
        self.slots = slots
