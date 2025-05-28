from typing import List

from app.data.Building import BuildingSlot
from app.data.ResourceField import ResourceField
from app.data.Storage import Storage


class Village:
    """docstring for Village."""

    def __init__(
        self,
        name: str,
        id: str,
        resource_fields: List[ResourceField],
        slots: List[BuildingSlot],
        storage: Storage,
    ):
        super(Village, self).__init__()
        self.name = name
        self.id = id
        self.resource_fields = resource_fields
        self.slots = slots
        self.storage = storage
        self.href = f"/dorf1.php?newdid={id}&"

    def to_dict(self):
        return {
            "name": self.name,
            "href": self.id,
            "resource_fields": [rf.to_dict() for rf in self.resource_fields],
            "slots": [slot.to_dict() for slot in self.slots],
            "storage": self.storage.to_dict(),
        }

    def __repr__(self):
        return (
            f"<Village (Name: {self.name}) (ID: {self.id}| Href:{self.href})>"
        )
