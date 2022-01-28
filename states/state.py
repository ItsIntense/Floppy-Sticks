class State(object):
    def __init__(self, manager):
        self.manager = manager
        self.setup()

    def setup(self):
        pass

    def update(self, events, **kwargs):
        pass

    def render(self, surface):
        pass
