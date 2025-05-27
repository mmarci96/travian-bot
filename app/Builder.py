class Builder:
    """docstring for Builder."""

    def __init__(self, browser, resources):
        super(Builder, self).__init__()
        self.browser = browser
        self.resources = resources

    def get_resources(self):
        return self.resources
