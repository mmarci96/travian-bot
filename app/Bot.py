import json
from random import randrange
from typing import List

from app import Chrome
from time import sleep
from datetime import datetime

from app.data import ResourceField
from app.Builder import Builder
from app.data.Building import BuildingSlot
from app.data.Granary import Granary
from app.data.ResourceAmount import ResourceAmount
from app.data.Storage import Storage
from app.data.Task import BuildingTask, ResourceTask
from app.data.Village import Village
from app.data.Warehouse import Warehouse


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


class Bot:
    def __init__(self, url, username, password):
        super(Bot, self).__init__()
        self.url = url
        self.username = username
        self.password = password
        self.browser = Chrome.Chrome(headless=False)
        self.villages: List[Village] = []

    def login(self):
        self.browser.goto(self.url)
        sleep(randrange(1, 2))
        self.browser.post({"name": self.username, "password": self.password})
        sleep(randrange(1, 2))
        self.browser.click("textButtonV2.green")
        sleep(randrange(1, 2))
        print("Logged into the account " + self.username)

    def go_home(self):
        self.browser.goto(self.url + "/dorf1.php")

    def go_village(self):
        self.browser.goto(self.url + "/dorf2.php")

    def go_to_village(self, village_href):
        self.browser.goto(self.url + village_href)

    def test_build(self):
        wood_upgrade_task = ResourceTask("crop", 7)
        if len(self.villages) == 0:
            print("No village")
            return

        for village in self.villages:
            print("[✓]Testing village: ", village)
            village.builder.add_res_task(wood_upgrade_task)
            self.go_to_village(village.get_href())
            sleep(randrange(1, 2))
            village.do_res_task()
            sleep(randrange(1, 2))

        second_village = self.villages[0]
        build_cranny_task = BuildingTask("30", "23")
        sleep(randrange(1, 2))
        second_village.add_build_task(build_cranny_task)
        self.go_to_village(second_village.get_href())
        sleep(1)
        second_village.do_building_task()

    def save_village_to_json(self, village: Village):
        filename = f"./data/village_{village.id}.json"
        with open(filename, "w") as f:
            json.dump(village.to_dict(), f, indent=2)
        print(f"[✓] Village data saved to {filename}")

    def setup(self):
        print("[+]Setup villages...")
        villages = self.browser.get_villages()
        for village in villages:
            village_id, village_name = next(iter(village.items()))
            self.load_village(village_id, village_name)

    def update(self):
        for village in self.villages:
            sleep(randrange(1, 2))
            self.go_to_village(village.__href)
            sleep(randrange(1, 3))
            village.do_res_task()
            sleep(randrange(1, 2))
            village.do_building_task()

    def load_village(self, id: str, name: str):
        """Scans the village by its ID and name populating the data for
        buildingslots, resource fields and tasks. Add instance to village list
        and saves stats to json"""
        sleep(randrange(1, 2))
        village_href = f"/dorf1.php?newdid={id}&"
        self.go_to_village(village_href)
        sleep(randrange(1, 2))
        res_fields = self.load_resources()
        slots = self.load_slots()
        store = self.load_storage()
        constructions = self.browser.get_building_list()
        print("constructions: ", constructions)
        sleep(randrange(1, 2))
        builder = Builder(self.browser, self.url, res_fields, slots)

        current_village = Village(
            name,
            id,
            builder,
            store,
        )
        self.villages.append(current_village)
        self.save_village_to_json(current_village)

    def load_slots(self) -> List[BuildingSlot]:
        """Gets the inner village html and parses Slots and its Building if
        present then returns it"""
        sleep(randrange(1, 3))
        self.browser.goto(self.url + "/dorf2.php")
        sleep(randrange(1, 2))
        slots = self.browser.get_building_slots()
        if slots:
            return slots
        return []

    def load_storage(self) -> Storage:
        """Fetch and populate Warehouse and Granary instances into Storage class
        in the current village then returns it"""
        sleep(randrange(1, 2))
        res = self.browser.get_resources()
        warehouse_resources = ResourceAmount(
            wood=res["wood"], clay=res["clay"], iron=res["iron"]
        )
        warehouse = Warehouse(res["warehouse_capacity"], warehouse_resources)
        granary = Granary(res["granary_capacity"], crop=res["crop"])
        storage = Storage(warehouse, granary)
        return storage

    def load_resources(self) -> List[ResourceField.ResourceField]:
        """Fetch and populate ResourceField the returns a list of the resouces
        of the village"""
        sleep(randrange(1, 2))
        res_fields_data = self.browser.get_resource_fields()

        resource_fields = []

        for res_type, fields in res_fields_data.items():
            for field in fields:
                resource = ResourceField.ResourceField(
                    resource_type=res_type,
                    slot=field["slot"],
                    href=field["href"],
                    level=field["level"],
                )
                resource_fields.append(resource)

        print(f"Loaded {len(resource_fields)} total resource fields.")
        return resource_fields

    def is_logged(self):
        return self.browser.current_url() != self.url
