# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Progress(Component):
    def __init__(self, *slots, max=None, value=None):
        self.attr({"max": max, "value": value})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="progress").proxy(self).render()
