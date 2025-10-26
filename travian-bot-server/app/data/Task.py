class ResourceTask:
    """docstring for ResourceTask."""

    def __init__(self, resouce_type: str, target_level: int):
        super(ResourceTask, self).__init__()
        self.resouce_type = resouce_type
        self.target_level = target_level

    def to_dict(self):
        return {
            "resource_type": self.resouce_type,
            "target_level": self.target_level,
        }

    def __repr__(self):
        return f"<Task (Resource: {self.resouce_type}), Target level: {self.target_level})>"


class BuildingTask:
    """docstring for BuildingTask."""

    def __init__(self, slot_id: str, building_id: str):
        super(BuildingTask, self).__init__()
        self.slot_id = slot_id
        self.building_id = building_id

    def to_dict(self):
        return {"slot_id": self.slot_id, "building_id": self.building_id}

    def __repr__(self):
        return f"<BuildingTask (SlotID: {self.slot_id}), BuildingID level: {self.building_id})>"
