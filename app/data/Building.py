class Building:
    """
    Represents a constructed building with an ID, name, and level.
    """

    def __init__(self, id: str, name: str, level: int):
        """
        Initialize a Building instance.

        Args:
            id (str): Unique identifier for the building.
            name (str): Name of the building.
            level (int): Current level of the building.
        """
        super(Building, self).__init__()
        self.id = id
        self.name = name
        self.level = level

    def get_name(self) -> str:
        """
        Returns the name of the building.

        Returns:
            str: The building's name.
        """
        return self.name

    def to_dict(self) -> dict:
        """
        Serializes the building instance to a dictionary.

        Returns:
            dict: Dictionary representation of the building.
        """
        return {"id": self.id, "name": self.name, "level": self.level}

    def __repr__(self) -> str:
        """
        Returns a string representation of the building.

        Returns:
            str: Readable summary of the building instance.
        """
        return f"<Building {self.id} (Name {self.name}) - Level {self.level}>"


class BuildingSlot:
    """
    Represents a slot on a map or UI where a building can be constructed.
    Contains an optional building instance and a reference href.
    """

    def __init__(self, slot_id: str, href: str):
        super(BuildingSlot, self).__init__()
        self.slot_id = slot_id
        self.href = href
        self.building: Building | None = None

    def set_building(self, building: Building):
        """
        Assigns a building to this slot.

        Args:
            building (Building): The building to associate with this slot.
        """
        self.building = building

    def get_href(self) -> str:
        """
        Returns the href associated with this slot.

        Returns:
            str: The href value.
        """
        return self.href

    def get_building(self) -> Building | None:
        """
        Returns the building assigned to this slot, if any.

        Returns:
            Building | None: The building object or None if unassigned.
        """
        return self.building

    def to_dict(self) -> dict:
        return {
            "slot_id": self.slot_id,
            "href": self.href,
            "building": self.building.to_dict() if self.building else None,
        }

    def __repr__(self) -> str:
        return f"<SlotID {self.slot_id} (Href: {self.href})>"
