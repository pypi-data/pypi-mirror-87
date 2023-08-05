# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Bdo(Component):
    def __init__(self, *slots, dir=None):
        self.attr({"dir": dir})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="bdo").proxy(self).render()
