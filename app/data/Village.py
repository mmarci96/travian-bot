from app.Builder import Builder
from app.data.Storage import Storage
from app.data.Task import BuildingTask, ResourceTask


class Village:
    """Village class can upgrade resources and build infrastructure."""

    def __init__(
        self,
        name: str,
        id: str,
        builder: Builder,
        storage: Storage,
    ):
        super(Village, self).__init__()
        self.name = name
        self.id = id
        self.storage = storage
        self.href = f"/dorf1.php?newdid={id}&"
        self.builder = builder

    def do_res_task(self):
        res_tasks = self.builder.get_res_tasks()
        if len(res_tasks) > 0:
            task = res_tasks[0]
            print("[-] Doing resource task: ", task)
            self.builder.build_lowest_resource(
                task.resouce_type, task.target_level
            )
            self.builder.remove_res_task(task)
        print("[✓] All resource upgrade tasks are finished!")

    def do_building_task(self):
        building_tasks = self.builder.get_build_tasks()
        if len(building_tasks) > 0:
            task = building_tasks[0]
            print("[-] Doing build task: ", task)
            self.builder.build_on_slot(task.slot_id, task.building_id)
            return
        print("[✓] All building tasks are finished!")

    def add_build_task(self, build_task: BuildingTask):
        self.builder.add_build_task(build_task)

    def add_res_task(self, resouce_task: ResourceTask):
        self.builder.add_res_task(resouce_task)

    def to_dict(self):
        return {
            "name": self.name,
            "href": self.id,
            "resource_fields": [
                rf.to_dict() for rf in self.builder.get_resources()
            ],
            "slots": [
                slot.to_dict() for slot in self.builder.get_build_slots()
            ],
            "storage": self.storage.to_dict(),
            "res_tasks": [
                rt.to_dict() for rt in self.builder.get_build_tasks()
            ],
            "build_task": [bt.to_dict() for bt in self.builder.get_res_tasks()],
        }

    def __repr__(self):
        return (
            f"<Village (Name: {self.name}) (ID: {self.id}| Href:{self.href})>"
        )
