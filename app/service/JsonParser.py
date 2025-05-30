import json
from typing import List

from app.data.DefaultLayout import Slot


class JsonParser:
    """docstring for JsonParser."""

    def __init__(self):
        super(JsonParser, self).__init__()

    def get_default_layout(self) -> List[Slot]:
        json_path = "../../data/village_layout.json"
        with open(json_path, "r") as file:
            data = json.load(file)

        # Optional: validation or transformation
        slots: List[Slot] = data.get("slots", [])
        return slots
