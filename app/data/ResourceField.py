class ResourceField:
    def __init__(self, resource_type: str, slot: int, href: str, level: int):
        self._resource_type = resource_type
        self._slot = slot
        self._href = href
        self._level = level

    # Getters
    def get_resource_type(self) -> str:
        return self._resource_type

    def get_slot(self):
        return self._slot

    def get_href(self) -> str:
        return self._href

    def get_level(self):
        return self._level

    # Setter for level
    def set_level(self, new_level):
        if isinstance(new_level, int) and new_level >= 0:
            self._level = new_level
        else:
            raise ValueError("Level must be a non-negative integer.")

    # Optional: readable string representation
    def __repr__(self):
        return f"<ResourceField {self._resource_type} (Slot {self._slot}) - Level {self._level}>"
