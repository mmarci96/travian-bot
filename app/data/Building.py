class Building:
    """docstring for Building."""

    def __init__(self, id: str, name: str, level: int):
        super(Building, self).__init__()
        self.id = id
        self.name = name
        self.level = level

    def get_name(self):
        return self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name, "level": self.level}

    def __repr__(self):
        return f"<Building {self.id} (Name {self.name}) - Level {self.level}>"


class BuildingSlot:
    """docstring for BuildingSlot."""

    def __init__(self, slot_id: str, href: str):
        super(BuildingSlot, self).__init__()
        self.slot_id = slot_id
        self.href = href
        self.building: Building | None = None

    def set_building(self, building: Building):
        self.building = building

    def get_href(self):
        return self.href

    def get_building(self) -> Building | None:
        return self.building

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "href": self.href,
            "building": self.building.to_dict() if self.building else None,
        }

    def __repr__(self):
        return f"<SlotID {self.slot_id} (Href: {self.href})>"
