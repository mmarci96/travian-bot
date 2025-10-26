from app.service.Builder import Builder
from app.data.Storage import Storage
from app.data.Task import BuildingTask, ResourceTask
from app.Logger import msg


class Village:
    """
    Represents a village capable of managing construction and resource upgrades
    via its Builder. Encapsulates storage, task management, and related metadata.
    """

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
        self.__href = f"/dorf1.php?newdid={id}&"
        self.builder = builder

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def update_data(self, builder: Builder, storage: Storage):
        self.builder = builder
        self.storage = storage

    def get_constructions(self):
        return self.builder.contructions

    def build_res_idle(self):
        constructions = self.builder.get_build_tasks()
        if len(constructions) == 0:
            msg("[-] No running construction, build lowest resource.")
            self.do_res_task()
        else:
            msg(f"[?] Constructions running: {constructions}")

    def do_res_task(self):
        """
        Execute the next resource upgrade task, if available.
        Removes the task after completion.
        """
        res_tasks = self.builder.get_res_tasks()
        if len(res_tasks) > 0:
            task = res_tasks[0]
            msg(f"[-] Doing resource task: {task}")
            self.builder.build_lowest_resource(
                task.resouce_type, task.target_level
            )
            resouces = self.builder.get_resources()
            is_done = False
            for resource in resouces:
                if (
                    resource.get_resource_type() == task.resouce_type
                    and resource.get_level() >= task.target_level
                ):
                    is_done = True

            if is_done:
                self.builder.remove_res_task(task)
            return
        msg("[✓] All resource upgrade tasks are finished!")

    def do_building_task(self):
        """
        Execute the next infrastructure building task, if available.
        Leaves task in queue for retry if construction fails.
        """
        building_tasks = self.builder.get_build_tasks()
        if len(building_tasks) > 0:
            task = building_tasks[0]
            msg(f"[-] Doing build task: {task}")
            self.builder.build_on_slot(task.slot_id, task.building_id)
            return
        msg("[✓] All building tasks are finished!")

    def add_build_task(self, build_task: BuildingTask):
        """
        Add a new building task to the queue.

        Args:
            build_task (BuildingTask): The building task to add.
        """
        self.builder.add_build_task(build_task)

    def add_res_task(self, resouce_task: ResourceTask):
        """
        Add a new resource task to the queue.

        Args:
            resouce_task (ResourceTask): The resource task to add.
        """
        self.builder.add_res_task(resouce_task)

    def get_href(self) -> str:
        """
        Get the internal link for this village.

        Returns:
            str: Href string used for navigation.
        """
        return self.__href

    def to_dict(self):
        """
        Serialize the Village and its components to a dictionary.

        Returns:
            dict: Dictionary representation of the village state.
        """
        return {
            "name": self.name,
            "id": self.id,
            "href": self.__href,
            "builder": self.builder.to_dict(),
            "storage": self.storage.to_dict(),
        }

    def __repr__(self):
        return (
            f"<Village (Name: {self.name}) (ID: {self.id}| Href:{self.__href})>"
        )
