from datetime import datetime, timedelta
import re
import traceback
from typing import Dict, List, Optional
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.data.Building import Building, BuildingSlot
from app.data.Construction import Construction
from app.Logger import msg


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
        except Exception:
            msg(f"[!] Failed to click element with class '{class_name}'")

    def get_by_classname(self, classname: str):
        return self.browser.find_elements(By.CLASS_NAME, value=classname)

    def get_buttons(self):
        return self.browser.find_elements(by=By.TAG_NAME, value="button")

    def get_links(self):
        return self.browser.find_elements(by=By.TAG_NAME, value="a")

    def get_build_command_by_id(self, building_id: str) -> Optional[str]:
        command = "/dorf2.php"
        try:
            id = "contract_building" + building_id
            container = self.browser.find_element(By.ID, id)
            btn_class = "textButtonV1.green.new"
            button = container.find_element(By.CLASS_NAME, btn_class)

            onclick_value = button.get_attribute("onclick")
            if onclick_value:
                match = re.search(r"'(.*?)'", onclick_value)
                if match:
                    command = match.group(1)
                    msg(f"[✓] ID: {building_id} | Parsed URL: {command}")
                else:
                    msg(f"[!] ID: {building_id} | No URL found in onclick.")
            return command
        except Exception:
            err_msg = (
                "Warning, not found element err, no valid command for buildID"
            )
            msg(f"[!] {err_msg}:{building_id}")

    def load_constructions(self) -> List[Construction]:
        building_list: List[Construction] = []
        try:
            list_cls = "buildingList"
            list_contianer = self.browser.find_element(By.CLASS_NAME, list_cls)
            if not list_contianer:
                return building_list
            li_elements = list_contianer.find_elements(By.TAG_NAME, "li")

            for li_elem in li_elements:
                t_cls = "buildDuration"
                timer_element = li_elem.find_element(By.CLASS_NAME, t_cls)
                time_str = timer_element.text
                done_at_match = re.search(r"done at (\d{2}:\d{2})", time_str)
                if not done_at_match:
                    raise ValueError("Invalid format")
                done_at_str = done_at_match.group(1)

                now = datetime.now()
                finish_time_today = datetime.strptime(
                    done_at_str, "%H:%M"
                ).replace(year=now.year, month=now.month, day=now.day)
                if finish_time_today < now:
                    finish_time_today += timedelta(days=1)

                name_element = li_elem.find_element(By.CLASS_NAME, "name")
                name = name_element.text
                lvl_elem = name_element.find_element(By.CLASS_NAME, "lvl")
                level = lvl_elem.text
                lvl = int(level[6:])

                if name and level:
                    c = Construction(name, lvl, finish_time_today)
                    msg(f"[-] Construction{c}")
                    building_list.append(c)

        except Exception:
            msg("[!] Failed to find element with class buildingList")
            traceback.print_exc()
        return building_list

    def get_villages(self) -> List[Dict[str, str]]:
        villages = []
        try:
            id = "sidebarBoxVillageList"
            list_elem = self.browser.find_element(By.ID, id)
            v_cls = "dropContainer"
            village_containers = list_elem.find_elements(By.CLASS_NAME, v_cls)

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

        except Exception:
            msg("[!] Failed to get village ids")
        return villages

    def get_building_slots(self) -> Optional[List[BuildingSlot]]:
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
            return building_slots
        except Exception:
            msg("[!] Failed to get building slot")

    def get_resource_fields(self):
        """Find all resource fields in the DOM and returns and Object of arrays,
        one for each resource type (wood, clay, iron, wheat)"""
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

                resource_type = None
                for cls in classes:
                    if cls in resource_field_classes:
                        resource_type = resource_field_classes[cls]
                        break

                if not resource_type:
                    continue

                level = 0
                slot = 0
                for cls in classes:
                    if cls.startswith("level") and len(cls) >= 6:
                        try:
                            level = int(cls[5:])  # Get number after 'level'
                        except ValueError:
                            msg(f"Not right value: {cls[5:]}")
                            pass
                        break

                for cls in classes:
                    if cls.startswith("buildingSlot") and len(cls) >= 13:
                        try:
                            slot = int(cls[12:])
                        except ValueError:
                            msg(f"Not right type: {cls[12:]}")
                            pass
                        break

                resource_fields[resource_type].append(
                    {
                        "href": href,
                        "slot": slot,
                        "level": level,
                    }
                )

        except Exception:
            msg("[!] Failed to get resource fields ")

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
                msg(f"[!] Failed to get {name}: {e}")
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
                msg("[!] Could not find both capacity values.")
                resources["warehouse_capacity"] = None
                resources["granary_capacity"] = None
        except Exception:
            msg("[!] Failed to get capacities")
            resources["warehouse_capacity"] = None
            resources["granary_capacity"] = None

        return resources

    def current_url(self) -> str:
        return self.browser.current_url
