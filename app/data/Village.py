from typing import List

from app.data.Building import BuildingSlot
from app.data.ResourceField import ResourceField
from app.data.Storage import Storage


class Village:
    """docstring for Village."""

    def __init__(
        self,
        name: str,
        href: str,
        resource_fields: List[ResourceField],
        slots: List[BuildingSlot],
        storage: Storage,
    ):
        super(Village, self).__init__()
        self.name = name
        self.href = href
        self.resource_fields = resource_fields
        self.slots = slots
        self.storage = storage

    def to_dict(self):
        return {
            "name": self.name,
            "href": self.href,
            "resource_fields": [rf.to_dict() for rf in self.resource_fields],
            "slots": [slot.to_dict() for slot in self.slots],
            "storage": self.storage.to_dict(),
        }
