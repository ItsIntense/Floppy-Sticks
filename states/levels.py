from states.state import State
from point import Point

class Levels(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.setup()

    def setup(self):
        pass

    def update(self, events):
        if events.get("keydown-escape"):
            self.manager.transition_to("menu")

    def render(self, surface):
        pass
