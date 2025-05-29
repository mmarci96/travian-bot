from random import randrange
import re
from time import sleep
from typing import List, Optional
from app.Chrome import Chrome
from app.data.Building import BuildingSlot
from app.data.ResourceField import ResourceField
from app.data.Task import BuildingTask, ResourceTask


class Builder:
    """Builder to handle building resources and infrastucture. Has a list of
    commads. Stores active contructions"""

    def __init__(
        self,
        browser: Chrome,
        base_url: str,
        resources: List[ResourceField],
        slots: List[BuildingSlot],
        building_tasks: List[BuildingTask] = [],
        res_tasks: List[ResourceTask] = [],
    ):
        super(Builder, self).__init__()
        self.browser = browser
        self.base_url = base_url
        self.resources = resources
        self.slots = slots
        self.building_tasks = building_tasks
        self.res_tasks = res_tasks

    def get_resources(self):
        return self.resources

    def get_build_tasks(self) -> List[BuildingTask]:
        return self.building_tasks

    def get_res_tasks(self) -> List[ResourceTask]:
        return self.res_tasks

    def get_build_slots(self) -> List[BuildingSlot]:
        return self.slots

    def get_slot_by_id(self, id: str) -> Optional[BuildingSlot]:
        for slot in self.get_build_slots():
            if slot.slot_id == id:
                return slot
        return None

    def remove_res_task(self, target_task: ResourceTask):
        task_list: List[ResourceTask] = []
        for task in self.res_tasks:
            if task.resouce_type != target_task:
                task_list.append(task)
        self.res_tasks.clear()
        self.res_tasks = task_list

    def remove_build_task(self, target_task: BuildingTask):
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
        """Add a resource task if it doesn't already exist."""
        if not any(
            existing_task.resouce_type == task.resouce_type
            for existing_task in self.res_tasks
        ):
            self.res_tasks.append(task)
        else:
            print("Task exists: ", self.res_tasks)

    def add_build_task(self, task: BuildingTask):
        """Add a building task if it's not a duplicate."""
        if not any(
            existing_task.building_id == task.building_id
            and existing_task.slot_id == task.slot_id
            for existing_task in self.building_tasks
        ):
            self.building_tasks.append(task)

    def build_lowest_resource(self, resource_type: str, target_level: int):
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
        sleep(1)
        slot = self.get_slot_by_id(slot_id)
        print("Build on slot: ", slot)
        if slot is None:
            print("no slot found")
            return
        target_url = slot.get_href()
        self.browser.goto(target_url)
        sleep(randrange(1, 2))
        command_target_url = self.browser.get_build_command_by_id(building_id)
        if command_target_url:
            sleep(randrange(1, 2))
            self.browser.goto(self.base_url + command_target_url)

    def new_building_on_slot(self, slot: BuildingSlot, building_name: str):
        print("New building with id: ", slot, building_name)

    def get_build_command(self) -> str:
        command = "/dorf1.php"
        buttons = self.browser.get_buttons()
        # print(f"Found {len(buttons)} button:")
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
            else:
                print(f"[-] {text} | No button matches returning:{command}")
        return command

    def to_dist(self):
        return {"builder": self.base_url}
