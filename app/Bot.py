from random import randrange

from app import Chrome
from time import sleep
from datetime import datetime

from app.data import ResourceField
from app.Builder import Builder
from app.data.Granary import Granary
from app.data.ResourceAmount import ResourceAmount
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

    def go_village(self):
        self.browser.goto(self.url + "/dorf2.php")
        sleep(1)
        slots = self.browser.get_building_slots()
        # print("SLOOOTS:", slots)
        for slot in slots:
            print("Slot: ", slot)
            building = slot.get_building()
            if building:
                print("Buidling found on slot: ", building)

    def setup(self):
        # sleep(randrange(1, 2))
        # self.load_storage()
        # self.load_resources()
        print("Setup villages...")
        villages = self.browser.get_villages()
        print("VillageIDs:", villages)

    def load_storage(self):
        res = self.browser.get_resources()
        warehouse_resources = ResourceAmount(
            wood=res["wood"], clay=res["clay"], iron=res["iron"]
        )
        self.warehouse = Warehouse(
            res["warehouse_capacity"], warehouse_resources
        )

        self.granary = Granary(res["granary_capacity"], crop=res["crop"])

    def load_resources(self):
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

    def test_builder(self):
        b = self.builder.get_resources()
        print("Builder", b)
        self.builder.build_lowest_resource()

    def test_store(self):
        gcap = self.granary.get_capacity()
        gcrop = self.granary.get_wheat()
        wcap = self.warehouse.get_capacity()
        wres = self.warehouse.get_resources()
        print("Granary: ", "capacity: " + str(gcap), "Crop:" + str(gcrop))
        print("Warehouse: ", "capacity: " + str(wcap), "Resources: ", wres)

    def is_logged(self):
        return self.browser.current_url() != self.url
