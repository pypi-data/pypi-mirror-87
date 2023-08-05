# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Br(Component):
    def __init__(self, *slots, clear=None):
        self.attr({"clear": clear})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="br").proxy(self).render()
