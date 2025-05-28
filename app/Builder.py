from random import randrange
import re
from time import sleep
from typing import List
from app.Chrome import Chrome
from app.data.Building import BuildingSlot
from app.data.ResourceField import ResourceField


class Builder:
    """docstring for Builder."""

    def __init__(
        self, browser: Chrome, resources: List[ResourceField], base_url: str
    ):
        super(Builder, self).__init__()
        self.browser = browser
        self.resources = resources
        self.base_url = base_url

    def get_resources(self):
        return self.resources

    def build_lowest_resource(self, resource_type="crop", target_level=5):
        lowest = None

        for res in self.resources:
            if res.get_resource_type() != resource_type:
                continue
            if res.get_level() >= target_level:
                continue
            if lowest is None or res.get_level() < lowest.get_level():
                lowest = res

        if lowest:
            print("Building resource:", lowest)
            sleep(1)
            self.browser.goto(lowest.get_href())
            sleep(randrange(2, 3))
            command = self.get_build_command()
            self.browser.goto(self.base_url + command)
            sleep(randrange(1, 2))
        else:
            print(
                f"No {resource_type} fields below level {target_level} found."
            )

    def build_on_slot(self, slot: BuildingSlot, building_id: str):
        target_url = slot.get_href()
        self.browser.goto(target_url)
        sleep(randrange(1, 2))
        target_url = self.browser.get_build_command_by_id(building_id)
        sleep(randrange(1, 2))
        self.browser.goto(target_url)

    def new_building_on_slot(self, slot: BuildingSlot, building_name: str):
        print("New building with id: ", slot, building_name)

    def get_build_command(self) -> str:
        command = "/dorf1.php"
        buttons = self.browser.get_buttons()
        print(f"Found {len(buttons)} button:")
        for button in buttons:
            text = (button.text or "").strip()
            if "level" in text.lower():
                onclick_value = button.get_attribute("onclick")
                if onclick_value:
                    match = re.search(r"'(.*?)'", onclick_value)
                    if match:
                        command = match.group(1)
                        print(f"[✓] {text} | Parsed URL: {command}")
                    else:
                        print(f"[!] {text} | No URL found in onclick.")

        return command
