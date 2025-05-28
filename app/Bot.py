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
        self.resource_fields = []
        self.builder = Builder(self.browser, self.resource_fields, self.url)

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

    def save_village_to_json(
        self, village: Village, filename="village_data.json"
    ):
        with open(filename, "w") as f:
            json.dump(village.to_dict(), f, indent=2)
        print(f"[✓] Village data saved to {filename}")

    def setup(self):
        print("Setup villages...")
        villages = self.browser.get_villages()
        print("VillageIDs:", villages)
        res_fields = self.load_resources()
        slots = self.load_slots()
        store = self.load_storage()
        self.current_village = Village(
            "idk", "/dorf1.php", res_fields, slots, store
        )
        # TODO test if current_village initiated
        print("Current village: ", self.current_village)
        self.save_village_to_json(self.current_village)

    def load_slots(self) -> List[BuildingSlot]:
        """Gets the inner village html and parses Slots and its Building if present"""
        sleep(randrange(1, 3))
        self.browser.goto(self.url + "/dorf2.php")
        sleep(randrange(1, 2))
        slots = self.browser.get_building_slots()
        return slots

    def load_storage(self) -> Storage:
        """Fetch and populate Warehouse and Granary instances into Storage class"""
        res = self.browser.get_resources()
        warehouse_resources = ResourceAmount(
            wood=res["wood"], clay=res["clay"], iron=res["iron"]
        )
        self.warehouse = Warehouse(
            res["warehouse_capacity"], warehouse_resources
        )

        self.granary = Granary(res["granary_capacity"], crop=res["crop"])
        storage = Storage(self.warehouse, self.granary)
        return storage

    def load_resources(self) -> List[ResourceField.ResourceField]:
        """Fetch and populate ResourceField instances into self.resource_fields"""
        sleep(randrange(1, 2))
        res_fields_data = self.browser.get_resource_fields()

        self.resource_fields.clear()

        for res_type, fields in res_fields_data.items():
            for field in fields:
                resource = ResourceField.ResourceField(
                    resource_type=res_type,
                    slot=field["slot"],
                    href=field["href"],
                    level=field["level"],
                )
                self.resource_fields.append(resource)

        print(f"Loaded {len(self.resource_fields)} total resource fields.")
        return self.resource_fields

    def is_logged(self):
        return self.browser.current_url() != self.url
