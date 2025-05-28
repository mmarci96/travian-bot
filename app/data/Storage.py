from app.data.Granary import Granary
from app.data.Warehouse import Warehouse


class Storage:
    """docstring for Storage."""

    def __init__(self, warehouse: Warehouse, granary: Granary):
        super(Storage, self).__init__()
        self.warehouse = warehouse
        self.granary = granary

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    def to_dict(self):
        return {
            "warehouse": self.warehouse.to_dict(),
            "granary": self.granary.to_dict(),
        }

    def get_granary(self) -> Granary:
        return self.granary
