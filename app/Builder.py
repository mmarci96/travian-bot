from typing import List
from app.Chrome import Chrome
from app.ResourceField import ResourceField


class Builder:
    """docstring for Builder."""

    def __init__(self, browser: Chrome, resources: List[ResourceField]):
        super(Builder, self).__init__()
        self.browser = browser
        self.resources = resources

    def get_resources(self):
        return self.resources

    def build_lowest_resource(self, resource_type="crop"):
        lowest = None
        for res in self.resources:
            if lowest is None:
                lowest = res
                continue
            if res.get_resource_type() == resource_type:
                if res.get_level() < lowest.get_level():
                    lowest = res

        print("Lowest resource: ", lowest)
        if lowest:
            self.browser.goto(lowest.get_href())
