# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Menu(Component):
    def __init__(self, *slots, type=None):
        self.attr({"type": type})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="menu").proxy(self).render()
