from app.data.ResourceAmount import ResourceAmount


class Warehouse:
    """docstring for Storage."""

    def __init__(self, capacity: int, resources: ResourceAmount):
        super(Warehouse, self).__init__()
        self.capacity = capacity
        self.resources = resources

    def get_capacity(self) -> int:
        return self.capacity

    def get_resource(self, resource_type: str) -> int:
        return getattr(self.resources, resource_type, 0)

    def get_resources(self) -> ResourceAmount:
        return self.resources

    def set_resources(self, resources: ResourceAmount):
        self.resources = resources

    def set_capacity(self, capacity: int):
        self.capacity = capacity
