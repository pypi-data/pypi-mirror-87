from ..component import Component


class Fragment(Component):
    def __init__(self, *slots):
        super().__init__(*slots)

    def render(self):
        return "".join([c.render() for c in self.slots])
