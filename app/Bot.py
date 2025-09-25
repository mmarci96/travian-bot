from random import randrange
from typing import Dict, List, Optional

from app import Chrome
from time import sleep
from datetime import datetime

from app.data import ResourceField
from app.data.DefaultLayout import DefaultLayout
from app.service.Builder import Builder
from app.data.Building import BuildingSlot
from app.data.Granary import Granary
from app.data.ResourceAmount import ResourceAmount
from app.data.Storage import Storage
from app.data.Task import ResourceTask
from app.data.Village import Village
from app.data.Warehouse import Warehouse
from app.service.JsonParser import JsonParser
from app.Logger import LogType, msg


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


class Bot:
    def __init__(self, url: str, username: str, password: str):
        super(Bot, self).__init__()
        self.url = url
        self.username = username
        self.password = password
        self.json_parser = JsonParser()
        self.browser = Chrome.Chrome(headless=True)
        self.villages: List[Village] = []
        self.default_layout = DefaultLayout(
            self.json_parser.get_default_layout(
                "./data/default_village_layout.json"
            )
        )
        self.military_village: Optional[Village] = None
        self.status = "init"

    def get_build_queue(self):
        build_queue = {}
        for village in self.villages:
            builder = village.builder
            # msg(f"village:{village.get_name()} - {village.get_id()}")
            # msg(f"build tasks:{builder.get_build_tasks()}")
            # msg(f"res tasks: {builder.get_res_tasks()}")
            constructions = builder.contructions
            build_queue[village.get_id()] = {"constructions": constructions}

        msg(f"[+] build_queue: {build_queue}")
        return build_queue

    def construct_building_by_name(self, village_id: str, building_name: str):
        msg(f"[+] build:{building_name}, village_id: {village_id}")
        village = None
        for v in self.villages:
            if v.get_id() == village_id:
                village = v
                break
        if village is None:
            msg(f"[-] no village found village_id: {village_id}", LogType.WARN)

        msg(f"[-] default_layout: {self.default_layout.slots}")

    def refresh_builds(self) -> Dict:
        msg("[-] refreshing builds")
        running_constructions = {}
        for village in self.villages:
            builder = village.builder
            builds = builder.get_build_tasks()
            res = builder.get_res_tasks()
            res_tasks = {}
            build_tasks = {}
            for r in res:
                res_tasks[r.resouce_type] = r.target_level
            for b in builds:
                existing = build_tasks.get(b.building_id)
                if existing:
                    build_tasks[b.building_id] = existing + 1
                else:
                    build_tasks[b.building_id] = 1
            msg(f"[+] res tasks: {res_tasks}")
            msg(f"[+] build tasks: {build_tasks}")
            running_constructions[village.get_id()] = {
                "res_tasks": res_tasks,
                "build_tasks": build_tasks,
            }

        msg(f"[+]{running_constructions}")
        return running_constructions

    def login(self):
        msg(f"Logging into game at url: {self.url}")
        self.browser.goto(self.url)
        sleep(randrange(1, 2))
        self.browser.post({"name": self.username, "password": self.password})
        sleep(randrange(1, 2))
        self.browser.click("textButtonV2.green")
        sleep(randrange(1, 2))
        msg("Logged into the account " + self.username)
        self.status = "idle"

    def get_status(self):
        return self.status

    def go_home(self):
        self.browser.goto(self.url + "/dorf1.php")

    def go_village(self):
        self.browser.goto(self.url + "/dorf2.php")

    def go_to_village(self, village_href):
        self.browser.goto(self.url + village_href)

    def setup(self):
        msg("[+] Setup villages...")
        villages = self.browser.get_villages()
        for village in villages:
            village_id, village_name = next(iter(village.items()))
            self.load_village(village_id, village_name)
        msg("[✓] Villages loaded")

    def update(self):
        msg("[✓] Started updating villages.")
        for village in self.villages:
            id = village.get_id()
            sleep(randrange(1, 2))
            village_href = f"/dorf1.php?newdid={id}&"
            self.go_to_village(village_href)
            msg(f"[✓] Navigate to current updating village:{village}")
            sleep(randrange(1, 2))
            res_fields = self.load_resources()
            store = self.load_storage()
            constructions = self.browser.load_constructions()
            sleep(randrange(1, 2))
            slots = self.load_slots()
            builder = Builder(
                self.browser, self.url, res_fields, slots, constructions
            )
            village.update_data(builder, store)
            village.build_res_idle()

    def build_resource(self, village_id: str, res_type: str, level: int) -> str:
        upgrade_task = ResourceTask(res_type, level)

        target_village = None
        for village in self.villages:
            if village.get_id() == village_id:
                target_village = village

        if target_village is None:
            return "village not found"

        msg(f"[✓] Adding task to village: {target_village}")
        village.builder.add_res_task(upgrade_task)
        self.go_to_village(target_village.get_href())
        sleep(randrange(1, 2))
        village.do_res_task()
        return "build task added"

    def test_build(self):
        upgrade_task = ResourceTask("crop", 7)
        if len(self.villages) == 0:
            msg("[!] No village found.")
            return

        for village in self.villages:
            msg(f"[✓] Testing village: {village}")
            village.builder.add_res_task(upgrade_task)
            self.go_to_village(village.get_href())
            sleep(randrange(1, 2))
            village.do_res_task()
            sleep(randrange(1, 2))

    def load_village(self, id: str, name: str):
        """Scans the village by its ID and name populating the data for
        buildingslots, resource fields and tasks. Add instance to village list
        and saves stats to json"""
        sleep(randrange(1, 2))
        village_href = f"/dorf1.php?newdid={id}&"
        self.go_to_village(village_href)
        sleep(randrange(1, 2))
        res_fields = self.load_resources()
        store = self.load_storage()
        constructions = self.browser.load_constructions()
        slots = self.load_slots()
        sleep(randrange(1, 2))
        builder = Builder(
            self.browser, self.url, res_fields, slots, constructions
        )

        current_village = Village(
            name,
            id,
            builder,
            store,
        )
        if name == "02":
            self.military_village = current_village
        self.villages.append(current_village)
        self.json_parser.save_village_to_json(current_village)

    def load_slots(self) -> List[BuildingSlot]:
        """Gets the inner village html and parses Slots and its Building if
        present then returns it"""
        sleep(randrange(1, 3))
        self.browser.goto(self.url + "/dorf2.php")
        sleep(randrange(1, 2))
        slots = self.browser.get_building_slots()
        if slots:
            msg("[✓] Loaded Slots from browser.")
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
        msg("[✓] Loaded Storage from browser.")
        return storage

    def load_resources(self) -> List[ResourceField.ResourceField]:
        """Fetch and populate ResourceField the returns a list of the resouces
        of the village"""
        resource_fields = []
        sleep(randrange(1, 2))
        res_fields_data = self.browser.get_resource_fields()

        for res_type, fields in res_fields_data.items():
            for field in fields:
                resource = ResourceField.ResourceField(
                    resource_type=res_type,
                    slot=field["slot"],
                    href=field["href"],
                    level=field["level"],
                )
                resource_fields.append(resource)

        msg("[✓] Loaded total resource fields.")
        return resource_fields

    def go_farmlist(self):
        self.browser.goto(self.url + "/build.php?id=39&gid=16&tt=99")
        sleep(randrange(3, 5))

    def send_list(self, list):
        if self.military_village:
            self.browser.goto(self.url + self.military_village.get_href())
            sleep(randrange(1, 2))
        self.browser.goto(self.url + "/build.php?id=39&gid=16&tt=99")
        sleep(randrange(3, 5))
        buttons = self.browser.get_by_classname(
            "textButtonV2.green.startButton"
        )
        for i in range(len(list)):
            index = int(list[i])
            buttons[index].click()
            msg("List #" + str(index) + " were sent")
            sleep(randrange(3, 5))

        msg(get_time() + ": Lists were sent")

    def get_villages(self):
        data = {}
        for village in self.villages:
            data[village.get_id()] = village.get_name()
        msg(f"[+] Villages: {data}")
        return {"villages": data}

    def get_constructions_by_village_id(self, village_id: str):
        village = None
        for v in self.villages:
            if v.get_id() == village_id:
                village = v
        if village is None:
            return None
        return village.get_constructions()

    def is_logged(self):
        return self.browser.current_url() != self.url
