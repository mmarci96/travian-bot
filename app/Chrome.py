from typing import Dict, List
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.data.Building import Building, BuildingSlot


class Chrome:
    path = "source/webdriver/chromedriver"

    def __init__(self, headless=True):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        self.browser = uc.Chrome(executable_path=self.path, options=options)

    def goto(self, url):
        self.browser.get(url)

    def post(self, params):
        for param in params:
            self.browser.find_element(by=By.NAME, value=param).send_keys(
                params[param]
            )

    def click(self, class_name, timeout=10):
        try:
            button = WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )
            button.click()
        except Exception as e:
            print(f"[!] Failed to click element with class '{class_name}': {e}")

    def get_buttons(self):
        return self.browser.find_elements(by=By.TAG_NAME, value="button")

    def get_links(self):
        return self.browser.find_elements(by=By.TAG_NAME, value="a")

    def get_villages(self) -> List[Dict[str, str]]:
        villages = []
        try:
            list_container = self.browser.find_element(
                By.ID, "sidebarBoxVillageList"
            )
            village_containers = list_container.find_elements(
                By.CLASS_NAME, "dropContainer"
            )
            for village_container in village_containers:

                village = village_container.get_attribute("data-sortid")
                if village:
                    village_id = village[7:]
                    name_elem = village_container.find_element(
                        By.XPATH,
                        f"//span[@class='name'][@data-did='{village_id}']",
                    )
                    name = name_elem.text
                    village_obj = {village_id: name}
                    villages.append(village_obj)

        except Exception as e:
            print(f"[!] Failed to get village ids: {e}")
        return villages

    def get_building_slots(self) -> List[BuildingSlot]:
        building_slots = []
        try:
            container = self.browser.find_element(By.ID, "villageContent")
            slots = container.find_elements(By.CLASS_NAME, "buildingSlot")

            for slot in slots:
                name = slot.get_attribute("data-name")
                slot_id = slot.get_attribute("data-aid")
                building_id = slot.get_attribute("data-gid")

                link = slot.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")
                level = link.get_attribute("data-level")

                if href and slot_id:
                    s = BuildingSlot(slot_id, href)
                    if name and building_id and level:
                        b = Building(building_id, name, int(level))
                        s.set_building(b)
                    building_slots.append(s)

        except Exception as e:
            print(f"[!] Failed to get building slot: {e}")

        return building_slots

    def get_resource_fields(self):
        resource_field_classes = {
            "gid1": "wood",
            "gid2": "clay",
            "gid3": "iron",
            "gid4": "crop",
        }

        resource_fields = {"wood": [], "clay": [], "iron": [], "crop": []}

        try:
            container = self.browser.find_element(
                By.ID, "resourceFieldContainer"
            )
            links = container.find_elements(By.TAG_NAME, "a")

            for link in links:
                class_attr = link.get_attribute("class")
                classes = class_attr.split() if class_attr else []
                href = link.get_attribute("href")

                # Match resource type
                resource_type = None
                for cls in classes:
                    if cls in resource_field_classes:
                        resource_type = resource_field_classes[cls]
                        break

                if not resource_type:
                    continue  # Skip if no known resource type

                level = 0
                slot = 0
                for cls in classes:
                    if cls.startswith("level") and len(cls) >= 6:
                        try:
                            level = int(cls[5:])  # Get number after 'level'
                        except ValueError:
                            print("Not right value: ", cls[5:])
                            pass
                        break

                for cls in classes:
                    if cls.startswith("buildingSlot") and len(cls) >= 13:
                        try:
                            slot = int(cls[12:])
                        except ValueError:
                            print("Not right type: ", cls[12:])
                            pass
                        break

                resource_fields[resource_type].append(
                    {
                        "href": href,
                        "slot": slot,
                        "level": level,
                    }
                )

        except Exception as e:
            print(f"[!] Failed to get resource fields: {e}")

        return resource_fields

    def get_resources(self) -> Dict[str, int]:
        resource_ids = {
            "wood": "l1",
            "clay": "l2",
            "iron": "l3",
            "crop": "l4",
            "free_crop": "stockBarFreeCrop",
        }

        resources = {}
        for name, element_id in resource_ids.items():
            try:
                elem = self.browser.find_element(By.ID, element_id)
                text = elem.text.strip()
                clean_text = (
                    text.replace("\u202d", "")
                    .replace("\u202c", "")
                    .replace(" ", "")
                    .replace(",", "")
                )
                resources[name] = int(clean_text)
            except Exception as e:
                print(f"[!] Failed to get {name}: {e}")
                resources[name] = None

        try:
            capacities = self.browser.find_elements(
                By.CSS_SELECTOR, "#stockBar .capacity .value"
            )
            if len(capacities) >= 2:
                warehouse = (
                    capacities[0]
                    .text.replace("\u202d", "")
                    .replace("\u202c", "")
                    .replace(" ", "")
                    .replace(",", "")
                )
                granary = (
                    capacities[1]
                    .text.replace("\u202d", "")
                    .replace("\u202c", "")
                    .replace(" ", "")
                    .replace(",", "")
                )
                resources["warehouse_capacity"] = int(warehouse)
                resources["granary_capacity"] = int(granary)
            else:
                print("[!] Could not find both capacity values.")
                resources["warehouse_capacity"] = None
                resources["granary_capacity"] = None
        except Exception as e:
            print(f"[!] Failed to get capacities: {e}")
            resources["warehouse_capacity"] = None
            resources["granary_capacity"] = None

        return resources

    def current_url(self) -> str:
        return self.browser.current_url
