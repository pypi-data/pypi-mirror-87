# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Slot(Component):
    def __init__(self, *slots, name=None):
        self.attr({"name": name})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="slot").proxy(self).render()
