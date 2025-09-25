import json
from typing import List

from app.data.DefaultLayout import Slot
from app.data.Village import Village


class JsonParser:
    """Parses JSON files to produce structured layout data."""

    def __init__(self):
        super(JsonParser, self).__init__()

    def get_default_layout(self, json_path: str) -> List[Slot]:
        with open(json_path, "r") as file:
            data = json.load(file)

        slots_data = data.get("slots", [])
        # print("Slots data: ", json.dumps(slots_data, indent=4))
        slots = []
        for slot_data in slots_data:
            slot_id = slot_data["slot_id"]
            building = slot_data["building"]
            if building:
                name = building["name"]
                id = building["id"]
                slot = Slot(slot_id, name, id)
                slots.append(slot)
            else:
                slot = Slot(slot_id)
                slots.append(slot)

        return slots

    def save_village_to_json(self, village: Village):
        filename = f"./data/village_{village.id}.json"
        with open(filename, "w") as f:
            json.dump(village.to_dict(), f, indent=2)
        print(f"[✓] Village data saved to {filename}")
