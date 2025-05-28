class Granary:
    """docstring for Granary."""

    def __init__(self, capacity: int, crop: int):
        super(Granary, self).__init__()
        self.capacity = capacity
        self.crop = crop

    def get_capacity(self) -> int:
        return self.capacity

    def get_wheat(self) -> int:
        return self.crop

    def set_wheat(self, wheat: int):
        self.crop = wheat

    def to_dict(self):
        return {"capacity": self.capacity, "crop": self.crop}

    def set_capacity(self, capacity: int):
        self.capacity = capacity
