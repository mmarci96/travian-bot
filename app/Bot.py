from random import randrange

from app import Chrome
from time import sleep
from datetime import datetime
import re

from app import ResourceField
from app.Builder import Builder


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
        self.builder = Builder(self.browser, self.resource_fields)

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

    def load_resources(self):
        """Fetch and populate ResourceField instances into self.resource_fields"""
        sleep(randrange(1, 2))
        res_fields_data = self.browser.get_resource_fields()
        print("Resource fields fetched.")

        self.resource_fields.clear()  # reset if reloading

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
        # for res in self.resource_fields:
        # print(res)

    def test_builder(self):
        b = self.builder.get_resources()
        print(b)
        self.builder.build_lowest_resource()

    def log_html(self):
        links = self.browser.get_links()
        print(f"Found {len(links)} links:")
        for a in links:
            print(f" - {a.text.strip()} | href={a.get_attribute('href')}")

    def log_resources(self):
        sleep(randrange(1, 2))
        resources = self.browser.get_resources()
        print("Resources: \n", resources)
        sleep(randrange(1, 2))
        res_fields = self.browser.get_resource_fields()
        print("Resource fields: \n", res_fields)
        res = res_fields["wood"][1]["href"]

        self.browser.goto(res)

        buttons = self.browser.get_buttons()
        print(f"Found {len(buttons)} button:")
        target_url = "/dorf1.php"
        for button in buttons:
            text = (button.text or "").strip()
            if "level" in text.lower():
                onclick_value = button.get_attribute("onclick")
                if onclick_value:
                    match = re.search(r"'(.*?)'", onclick_value)
                    if match:
                        target_url = match.group(1)
                        print(f"[✓] {text} | Parsed URL: {target_url}")
                    else:
                        print(f"[!] {text} | No URL found in onclick.")
        sleep(1)
        self.browser.goto(self.url + target_url)
        sleep(5)

    def is_logged(self):
        return self.browser.current_url() != self.url
