# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Ol(Component):
    def __init__(self, *slots, reversed=None, start=None, type=None):
        self.attr({"reversed": reversed, "start": start, "type": type})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="ol").proxy(self).render()
