from typing import List

from app.data.Building import BuildingSlot
from app.data.ResourceField import ResourceField
from app.data.Storage import Storage
from app.data.Task import BuildingTask, ResourceTask


class Village:
    """docstring for Village."""

    def __init__(
        self,
        name: str,
        id: str,
        resource_fields: List[ResourceField],
        slots: List[BuildingSlot],
        storage: Storage,
        res_task: List[ResourceTask] = [],
        build_task: List[BuildingTask] = [],
    ):
        super(Village, self).__init__()
        self.name = name
        self.id = id
        self.resource_fields = resource_fields
        self.slots = slots
        self.storage = storage
        self.href = f"/dorf1.php?newdid={id}&"
        self.res_task = res_task
        self.build_task = build_task

    def get_build_tasks(self) -> List[BuildingTask]:
        return self.build_task

    def get_res_tasks(self) -> List[ResourceTask]:
        return self.res_task

    def remove_res_task(self, target_task: ResourceTask):
        task_list: List[ResourceTask] = []
        for task in self.res_task:
            if task.resouce_type != target_task:
                task_list.append(task)
        self.res_task.clear()
        self.res_task = task_list

    def remove_build_task(self, target_task: BuildingTask):
        task_list: List[BuildingTask] = []
        for task in self.build_task:
            if (
                task.building_id != target_task.building_id
                and task.slot_id != target_task.slot_id
            ):
                task_list.append(task)
        self.build_task.clear()
        self.build_task = task_list

    def add_res_task(self, task: ResourceTask):
        """Add a resource task if it doesn't already exist."""
        if not any(
            existing_task.resouce_type == task.resouce_type
            for existing_task in self.res_task
        ):
            self.res_task.append(task)

    def add_build_task(self, task: BuildingTask):
        """Add a building task if it's not a duplicate."""
        if not any(
            existing_task.building_id == task.building_id
            and existing_task.slot_id == task.slot_id
            for existing_task in self.build_task
        ):
            self.build_task.append(task)

    def to_dict(self):
        return {
            "name": self.name,
            "href": self.id,
            "resource_fields": [rf.to_dict() for rf in self.resource_fields],
            "slots": [slot.to_dict() for slot in self.slots],
            "storage": self.storage.to_dict(),
            "res_tasks": [rt.to_dict() for rt in self.build_task],
            "build_task": [bt.to_dict() for bt in self.res_task],
        }

    def __repr__(self):
        return (
            f"<Village (Name: {self.name}) (ID: {self.id}| Href:{self.href})>"
        )
