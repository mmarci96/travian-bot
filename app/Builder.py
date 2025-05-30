from random import randrange
import re
from time import sleep
from typing import List, Optional
from app.Chrome import Chrome
from app.data.Building import BuildingSlot
from app.data.Construction import Construction
from app.data.ResourceField import ResourceField
from app.data.Task import BuildingTask, ResourceTask


class Builder:
    """
    Builder manages the construction of resource fields and infrastructure.
    It handles building slots, active constructions, and task queues for both
    buildings and resource fields.
    """

    def __init__(
        self,
        browser: Chrome,
        base_url: str,
        resources: List[ResourceField],
        slots: List[BuildingSlot],
        contructions: List[Construction],
        building_tasks: List[BuildingTask] = [],
        res_tasks: List[ResourceTask] = [],
    ):
        super(Builder, self).__init__()
        self.browser = browser
        self.base_url = base_url
        self.resources = resources
        self.slots = slots
        self.contructions = contructions
        self.building_tasks = building_tasks
        self.res_tasks = res_tasks

    def get_resources(self):
        """
        Returns the list of resource fields managed by the builder.
        Returns:
            List[ResourceField]: List of resource fields.
        """
        return self.resources

    def get_build_tasks(self) -> List[BuildingTask]:
        """
        Returns the queue of scheduled building tasks.

        Returns:
            List[BuildingTask]: Building tasks to be executed.
        """
        return self.building_tasks

    def get_res_tasks(self) -> List[ResourceTask]:
        """
        Returns the queue of scheduled resource field tasks.

        Returns:
            List[ResourceTask]: Resource field tasks to be executed.
        """
        return self.res_tasks

    def get_build_slots(self) -> List[BuildingSlot]:
        """
        Returns the available building slots.

        Returns:
            List[BuildingSlot]: Building slots.
        """
        return self.slots

    def get_slot_by_id(self, id: str) -> Optional[BuildingSlot]:
        """
        Retrieve a building slot by its ID.

        Args:
            id (str): The slot ID to search for.

        Returns:
            Optional[BuildingSlot]: The matching slot or None if not found.
        """
        for slot in self.get_build_slots():
            if slot.slot_id == id:
                return slot
        return None

    def remove_res_task(self, target_task: ResourceTask):
        """
        Remove a resource task from the queue based on its resource type.

        Args:
            target_task (ResourceTask): The task to remove.
        """
        task_list: List[ResourceTask] = []
        for task in self.res_tasks:
            if task.resouce_type != target_task:
                task_list.append(task)
        self.res_tasks.clear()
        self.res_tasks = task_list

    def remove_build_task(self, target_task: BuildingTask):
        """
        Remove a building task from the queue based on building and slot ID.

        Args:
            target_task (BuildingTask): The task to remove.
        """
        task_list: List[BuildingTask] = []
        for task in self.building_tasks:
            if (
                task.building_id != target_task.building_id
                and task.slot_id != target_task.slot_id
            ):
                task_list.append(task)
        self.building_tasks.clear()
        self.building_tasks = task_list

    def add_res_task(self, task: ResourceTask):
        """
        Add a resource task if it doesn't already exist.

        Args:
            task (ResourceTask): The task to add.
        """
        if not any(
            existing_task.resouce_type == task.resouce_type
            for existing_task in self.res_tasks
        ):
            self.res_tasks.append(task)
        else:
            print("Task exists: ", self.res_tasks)

    def add_build_task(self, task: BuildingTask):
        """
        Add a building task if it is not a duplicate.

        Args:
            task (BuildingTask): The task to add.
        """
        if not any(
            existing_task.building_id == task.building_id
            and existing_task.slot_id == task.slot_id
            for existing_task in self.building_tasks
        ):
            self.building_tasks.append(task)

    def build_lowest_resource(self, resource_type: str, target_level: int):
        """
        Automatically find and build the lowest-level resource field
        of a given type that is below the target level.

        Args:
            resource_type (str): The resource type to upgrade (e.g. wood, clay).
            target_level (int): The target level to reach.
        """
        lowest = None
        for res in self.resources:
            if res.get_resource_type() != resource_type:
                continue
            if res.get_level() >= target_level:
                continue
            if lowest is None or res.get_level() < lowest.get_level():
                lowest = res

        if lowest:
            print("[-]Building lowest resource found: ", lowest)
            sleep(1)
            self.browser.goto(lowest.get_href())
            sleep(randrange(2, 3))
            command = self.get_build_command()
            self.browser.goto(self.base_url + command)
            sleep(randrange(1, 2))
        else:
            print(
                f"[!]No {resource_type} fields below level {target_level} found."
            )

    def build_on_slot(self, slot_id: str, building_id: str):
        """
        Build a structure on a given building slot.

        Args:
            slot_id (str): ID of the slot to build on.
            building_id (str): ID of the building to construct.
        """
        sleep(1)
        slot = self.get_slot_by_id(slot_id)
        print("[+] Build on slot: ", slot)
        if slot is None:
            print("[!] No slot found")
            return
        target_url = slot.get_href()
        self.browser.goto(target_url)
        sleep(randrange(1, 2))
        command_target_url = self.browser.get_build_command_by_id(building_id)
        if command_target_url:
            sleep(randrange(1, 2))
            self.browser.goto(self.base_url + command_target_url)

    def get_build_command(self) -> str:
        """
        Parse the current page and return the first usable build command
        from a button with an 'onclick' attribute.

        Returns:
            str: The relative URL command to trigger building.
        """
        command = "/dorf1.php"
        buttons = self.browser.get_buttons()
        for button in buttons:
            text = (button.text or "").strip()
            if "level" in text.lower():
                onclick_value = button.get_attribute("onclick")
                if onclick_value:
                    match = re.search(r"'(.*?)'", onclick_value)
                    if match and match.group(1) != "disabled":
                        command = match.group(1)
                        print(f"[✓] {text} | Parsed URL: {command}")
                    else:
                        print(f"[!] {text} | No URL found in onclick.")
        return command

    def to_dict(self):
        """
        Serializes the builder and its components to a dictionary.

        Returns:
            dict: Dictionary representation of the builder state.
        """
        return {
            "base_url": self.base_url,
            "resources": [r.to_dict() for r in self.resources],
            "slots": [s.to_dict() for s in self.slots],
            "constructions": [c.to_dict() for c in self.contructions],
            "building_tasks": [b.to_dict() for b in self.building_tasks],
            "resource_tasks": [r.to_dict() for r in self.res_tasks],
        }
