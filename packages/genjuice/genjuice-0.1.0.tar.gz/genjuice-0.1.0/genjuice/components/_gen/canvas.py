# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Canvas(Component):
    def __init__(self, *slots, height=None, width=None):
        self.attr({"height": height, "width": width})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="canvas").proxy(self).render()
